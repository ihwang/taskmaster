# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterd.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:24:46 by tango             #+#    #+#              #
#    Updated: 2020/08/26 02:31:50 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import os
import sys
import queue
import threading
import signal
import logging as log

from src.branch_execute import *
from src.go_daemon import *
from src.server import *
from src.programs import *
from src.feedback import recvall, recv_one_message, send_one_message

g_programs = list()
server = None
execute = None

def stopsignal_handler(signum, frame):
    log.info("server: Detected %(sig)d signal has been sent", {"sig": signum})
    global g_programs
    for p in g_programs:
        if p._stopsignal == signum:
            log.info("server: %(pid)d will be stopeed after %(sec)d sec", {"pid": p._pid.pid, "sec": p._stoptime})
            try:
                p._pid.wait(p._stoptime)
            except subprocess.TimeoutExpired:
                p._pid.terminate()

def listen_sighup(signum, frame):
    g_programs = create_configured_programs(server._config)
    execute.load_programs(g_programs)

def listen_other_signals(signum, frame):
    log.info("server: Detected %(sig)d signal has been sent", {"sig": signum})
    global g_programs
    for p in g_programs:
        if p._stopsignal == signum:
            log.info("server: %(pid)d will be stoped after %(sec)d sec", {"pid": p._pid.pid, "sec": p._stoptime})
            try:
                p._pid.wait(p._stoptime)
            except subprocess.TimeoutExpired:
                p._pid.terminate()
                log.info("server: %(pid)d \'%(n)s\' was killed", {"pid": p._pid.pid, "n": p._name})
    if signum == signal.SIGTERM:
        exit(0)

def listen_signals():
    signal.signal(signal.SIGHUP, listen_sighup)
    signal.signal(signal.SIGINT, listen_other_signals)
    signal.signal(signal.SIGTERM, listen_other_signals)
    signal.signal(signal.SIGQUIT, listen_other_signals)

def main():
    global g_programs
    global server
    global execute

    go_daemon()
    server = Server()
    server.start()
    g_programs = create_configured_programs(server._config)
    log.info("server: A config file has been loaded")
    execute = Execute(g_programs)
    execute.auto_start(server)
    listen_signals()

    while True:
        execute.reload_status = False
        job = recv_one_message(server._conn)
        if job == "disconnected":
            log.info("The client %(addr)s has been disconnected", {"addr": server._client_addr})
            server.wait_for_connect()
            g_programs = create_configured_programs(server._config)
            execute.load_programs(g_programs)
            execute.auto_start(server)
        else:
            execute.execute_msg(execute, server, job)
            
if __name__ == "__main__":
    main()
