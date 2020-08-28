# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmasterctl.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:24:41 by tango             #+#    #+#              #
#    Updated: 2020/08/29 00:08:50 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import yaml
import sys
import cmd
import logging as log
import socket
import threading
import time
import getpass
from os import EX_NOHOST

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

        try:
            fd = open(port_file, "r", encoding="utf-8")
        except FileNotFoundError:
            print("taskmasterctl: \'taskmasterd.py\' should be ", end="", file=sys.stderr)
            print("launched first (" + port_file + " doesn't exsist)", file=sys.stderr)
            exit(EX_NOHOST)
        portnb = fd.readline()
        fd.close()
        self._sock = socket.socket()
        log.info("client: Trying to connect to the server")
        try:
            self._sock.connect(("127.0.0.1", int(portnb)))
        except:
            log.error("client: Unable to connect to the server")
            print("taskmasterctl: \'taskmasterd.py\' should be launched first", file=sys.stderr)
            exit(EX_NOHOST)
        log.info("client: Taskmaster control shell has been connected to the server")
    
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
        log.info("client: Request to reload")
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
        log.info("client: Request to send status info of %(n)s", {"n": name})
        status = "status"
        send_one_message(self.client._sock, status)
        send_one_message(self.client._sock, name)
        time.sleep(0.01)

    def do_start(self, name):
        'usage: start programname (with no whitespace)'
        log.info("client: Request to execute %(n)s", {"n": name})
        if len(name) == 0:
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
        log.info("client: Request to restart %(n)s", {"n": name})
        if len(name) == 0:
            print("usage: restart programname", file=sys.stderr)
        elif " " in name:
            print("taskmasterctl: Possible to take only one arg", file=sys.stderr)
        else:
            restart = "restart"
            send_one_message(self.client._sock, restart)
            send_one_message(self.client._sock, name)
            time.sleep(0.01)
    
    def do_stop(self, name):
        'usage: stop programname (with no whitesppace)'
        log.info("client: Request to stop %(n)s", {"n": name})
        if len(name) == 0:
            print("usage: restart programname", file=sys.stderr)
        elif " " in name:
            print("taskmasterctl: Possible to take only one arg", file=sys.stderr)
        else:
            stop = "stop"
            send_one_message(self.client._sock, stop)
            send_one_message(self.client._sock, name)
            time.sleep(0.01)
    
    def do_setmail(self, name):
        'Setting email accounts for sending and receiving the result of executions'
        log.info("client: Request to set email addresses")
        my_addr = input("Your email Address: ")
        passwd = getpass.getpass()
        to_addr = input("The recipient's Address: ")
        send_one_message(self.client._sock, "setmail")
        send_one_message(self.client._sock, my_addr)
        send_one_message(self.client._sock, passwd)
        send_one_message(self.client._sock, to_addr)
    
    def do_unsetmail(self, name):
        'Unset pre-configured email address'
        log.info("client: Request to unset email addresses")
        send_one_message(self.client._sock, "unsetmail")

def find_space(raw_yaml):
    for key in raw_yaml["program"]:
        if ' ' in key:
            return key
    return False

def get_check_raw_yaml():
    if sys.argv[1][-5:] != ".yaml":
        print("taskmasterctl: The config file is not a yaml file", file=sys.stderr)
        return False
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
