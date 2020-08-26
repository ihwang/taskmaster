# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    branch_execute.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:24:58 by tango             #+#    #+#              #
#    Updated: 2020/08/26 19:33:29 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging as log
import os
import subprocess
import time
import threading
import signal

from src.server import *
from src.programs import *
from src.status import *
from src.feedback import recvall, recv_one_message, send_one_message

class Execute:
    def __init__(self, programs):
        self._programs = programs
        self.reload_status = False

    def reload(self, server):
        self.reload_status = True
        server.get_config()
        programs = create_configured_programs(server._config)
        self._programs = programs
        log.info("server: A config file has been reloaded")
        self.auto_start(server)

    def status(self, name, server):
        log.info("server: %(n)s\'s status has been requested to be sent to client", {"n": name})
        send_status(self._programs, name, server)

    def start(self, name, server):
        ever_started = False
        for p in self._programs:
            if p._name == name and p._start_status != "NotStarted":
                feedback = name + " has been already started. Try \'restart\' or \'status\'"
                send_one_message(server._conn, "feedback_start")
                log.info("server: %(n)s has been already started.", {"n": name})
                send_one_message(server._conn, feedback)
                return
            elif p._name == name:
                log.info("server: The name of the program should be executed is %(pn)s", {"pn": p._name})
                ever_started = True
                threading.Thread(target=self.run_program, args=(p,), daemon=True).start()
        if ever_started is False:
            log.info("server: Not able to find such program name")
            send_one_message(server._conn, "feedback_start")
            send_one_message(server._conn, "server: Not able to find such program name")

    def restart(self, name, server):
        ever_started = False
        for p in self._programs:
            if p._name == name and (p._start_status == "Exited" or p._start_status == "Stopped"):
                log.info("server: The name of the program should be restart is %(pn)s", {"pn": p._name})
                ever_started = True
                threading.Thread(target=self.run_program, args=(p,), daemon=True).start()
            elif p._name == name and (p._start_status == "NotStarted" or p._start_status == "Running"):
                feedback = name + " is on running or never started. Try \'status\' or \'start\'"
                log.info("server: %(n)s is on running or never started.", {"n": name})
                send_one_message(server._conn, "feedback_restart")
                send_one_message(server._conn, feedback)
                return
        if ever_started is False:
            log.info("server: Not able to find such program name")
            send_one_message(server._conn, "feedback_restart")
            send_one_message(server._conn, "Not able to find such program name")
    
    def stop(self, name, server):
        ever_stopped = False
        for p in self._programs:
            if p._name == name and p._start_status == "Running":
                log.info("server: The name of the program should be stopped is %(pn)s", {"pn": p._name})
                p._start_status = "Stopped"
                p._pid.terminate()
                ever_stopped = True
            elif p._name == name:
                log.info("server: %(n)s is not running at this moment")
                feedback = name + " is not running at this moment"
                send_one_message(server._conn, "feedback_stop")
                send_one_message(server._conn, feedback)
                return
        if ever_stopped is False:
            log.info("server Not able to find such program name")
            send_one_message(server._conn, "feedback_stop")
            send_one_message(server._conn, "Not able to find such program name")

    def run_program(self, prog):
        retry_count = 0
        temp_umask = os.umask(prog._umask)
        while True:
            self.redirect_stdout_stderr(prog)
            os.umask(prog._umask)
            prog._start_status = "Running"
            prog._pid = subprocess.Popen(prog._cmd,
                                stdout=prog._stdout_fd,
                                stderr=prog._stderr_fd,
                                close_fds=False,
                                cwd=prog._workingdir,
                                env=prog._env)
            log.info("server: %(name)s has been executed", {"name": prog._name})
            try:
                prog._pid.wait(prog._starttime)
            except subprocess.TimeoutExpired:
                log.info("server: %(n)s has been successfully launched", {"n": prog._name})
                flag_timeout = True
                prog._pid.wait()
                log.info("server: %(n)s has been successfully terminated", {"n": prog._name})
            else:
                log.info("server: %(n)s failed. Terminated in \'starttime\' %(s)d sec", {"n": prog._name, "s": prog._starttime})
                flag_timeout = False
            prog._start_status = "Exited"
            if self.reload_status is True:
                log.info("server: %(n)s will not be restarted since the config has been reloaded")
                break
            elif prog._autorestart == True:
                log.info("server: Trying to restart %(n)s since \'autorestart\' option has been given", {"n": prog._name})
                continue
            elif prog._autorestart == "unexpected":
                if retry_count < prog._startretries and \
                    (prog._exitcode != prog._pid.returncode or flag_timeout is False):
                    retry_count += 1
                    log.info("server: Trying to restart %(n)s since \'exitcode\' is not matched", {"n": prog._name})
                    continue
            break
        os.umask(temp_umask)

    def redirect_stdout_stderr(self, p):
        if p._stdout == "discard":
            p._stdout_fd = subprocess.DEVNULL
        else:
            p._stdout_fd = open(p._stdout, "a", encoding="utf-8")
            os.chmod(p._stdout, 0o644)
        if p._stderr == "discard":
            p._stderr_fd = subprocess.DEVNULL
        else:
            p._stderr_fd = open(p._stderr, "a", encoding="utf-8")
            os.chmod(p._stderr, 0o644)

    def auto_start(self, server):
        log.info("server: \'auto_start\' has been executed")
        for p in self._programs:
            if p._autostart is True:
                self.start(p._name, server)
    
    def load_programs(self, programs):
        self._programs = programs

    def execute_msg(self, execute, server, job):
        log.info("server: The requested job is %(job)s", {"job": job})
        if job == "reload":
            self.reload(server)
        else:
            name = recv_one_message(server._conn)
            if job == "status":
                self.status(name, server)
            elif job == "start":
                self.start(name, server)
            elif job == "restart":
                self.restart(name, server)
            elif job == "stop":
                self.stop(name, server)
