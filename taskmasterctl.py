# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterctl.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:24:41 by tango             #+#    #+#              #
#    Updated: 2020/08/26 02:34:41 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import yaml
import sys
import cmd
import logging as log
import socket
import threading
import time

from src.feedback import *

port_file = "/tmp/.TM_port_server"
log_file = "/tmp/TM_log.txt"

class Client():
    def __init__(self):
        log.basicConfig(level=log.DEBUG,
                        format="[%(asctime)s][%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=log_file)
        log.info("client: Taskmaster control shell is started")

        with open(port_file, "r", encoding="utf-8") as fd:
            portnb = fd.readline()
        self._sock = socket.socket()
        self._sock.connect(("127.0.0.1", int(portnb)))
        log.info("client: Taskmaster control shell is connected to the server")
    
    def send_config(self, config):
        data = yaml.dump(config).encode("utf-8")
        self._sock.sendall(data)

class Commands(cmd.Cmd):
    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.intro = "\nWelcome to Taskmaster. Try \'help\' or \'?\' to see the available commands"
        self.prompt = "Taskmaster$> "
        self.doc_header = "Availiable commands"
        #self._reload_status = False
        cmd.Cmd.emptyline(self)

        self.client = client

    def emptyline(self):
        pass

    def do_exit(self, notused):
        'exit the taskmaster shell'
        discon = "disconnected"
        send_one_message(self.client._sock, discon)
        exit(0)

    def do_reload(self, notused):
        'update the configuration file to the changed'
        config = get_check_raw_yaml()
        if len(notused) > 0:
            print("taskmasterctl: Retry with no arguments", file=sys.stderr)
        if config == False:
            pass
        else:
            re = "reload"
            send_one_message(self.client._sock, re)
            self.client.send_config(config)

    def do_status(self, name):
        'usage: status [programname]\nNo argument will get every single status'
        status = "status"
        send_one_message(self.client._sock, status)
        log.debug("client: sent the server requesting status")
        send_one_message(self.client._sock, name)
        time.sleep(0.01)

    def do_start(self, name):
        'usage: start programname (with no whitespace)'
        if len(name) < 1:
            print("usage: start programname", file=sys.stderr)
        elif " " in name:
            print("taskmasterctl: Possible to take only one arg", file=sys.stderr)
        else:
            start = "start"
            send_one_message(self.client._sock, start)
            send_one_message(self.client._sock, name)
            time.sleep(0.01)

    def do_restart(self, name):
        'usage: restart programname (with no whitespace)'
        if len(name) < 1:
            print("usage: restart programname", file=sys.stderr)
        elif " " in name:
            print("taskmasterctl: Possible to take only one arg", file=sys.stderr)
        else:
            restart = "restart"
            send_one_message(self.client._sock, restart)
            send_one_message(self.client._sock, name)
            time.sleep(0.01)
    
    def do_stop(self, name):
        'stop'

def find_space(raw_yaml):
    for key in raw_yaml["program"]:
        if ' ' in key:
            return key
    return False

def get_check_raw_yaml():
    with open(sys.argv[1], "rt") as stream:
        raw_yaml = yaml.safe_load(stream)

    wrong_name = find_space(raw_yaml)
    if "program" not in raw_yaml:
        print("taskmasterctl: Wrong config \'program:\' sholud be preceedded", file=sys.stderr)
        return False
    elif wrong_name != False:
        print("taskmasterctl: A white space is not allowed in the program name \'", wrong_name,
            "\'", sep="", file=sys.stderr)
        return False
    elif raw_yaml["program"] == None:
        print("taskmasterctl: Specify one program at least under the \'program\'", file=sys.stderr)
        return False
    for key, value in raw_yaml["program"].items():
        if "cmd" not in value:
            print("taskmasterctl: the program \'", key, "\' needs a \'cmd\' to execute", sep="", file=sys.stderr)
            return False
    return raw_yaml


def main():
    if len(sys.argv) != 2:
        print("taskmasterctl: Usage: taskmaster.py [configfile]", file=sys.stderr)
        exit(1)
    config = get_check_raw_yaml()
    if config == False:
        exit(1)
    client = Client()
    threading.Thread(target=feedback_listener, args=(client._sock,), daemon=True).start()
    client.send_config(config)
    tm_shell = Commands(client)
    tm_shell.cmdloop()

if __name__ == "__main__":
    main()
