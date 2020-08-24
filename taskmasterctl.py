import yaml
import sys
import cmd
import logging as log
import socket
import threading
import time

from feedback import *

BUFF_SIZE = 4096
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
        if config == False:
            pass
        else:
            re = "reload"
            send_one_message(self.client._sock, re)
            self.client.send_config(config)

    def do_status(self, name):
        'status'
        status = "status"
        self.client._sock.sendall(status.encode())
        self.client._sock.sendall(name.encode())

    def do_start(self, name):
        'start'
        start = "start"
        send_one_message(self.client._sock, start)
        send_one_message(self.client._sock, name)
        time.sleep(0.01)

    def do_restart(self, name):
        'restart'
        restart = "restart"
        self.client._sock.sendall(restart.encode())
        self.client._sock.sendall(name.encode())

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
        print("taskmaster: Wrong config \'program:\' sholud be preceedded", file=sys.stderr)
        return False
    elif wrong_name != False:
        print("A white space is not allowed in the program name \'", wrong_name,
            "\'", sep="", file=sys.stderr)
        return False
    elif raw_yaml["program"] == None:
        print("taskmaster: Specify one program at least under the \'program\'", file=sys.stderr)
        return False
    for key, value in raw_yaml["program"].items():
        if "cmd" not in value:
            print("taskmaster: the program \'", key, "\' needs a \'cmd\' to execute", sep="", file=sys.stderr)
            return False
    return raw_yaml


def main():
    if len(sys.argv) != 2:
        print("taskmaster: Usage: taskmaster.py [configfile]", file=sys.stderr)
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