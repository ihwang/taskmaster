# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    programs.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:09 by tango             #+#    #+#              #
#    Updated: 2020/08/29 22:39:06 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import yaml
import signal
from copy import deepcopy

class Program:
    def __init__(self, name, cmd):

        #Configurable values
        self._name = name
        self._cmd = cmd
        self._numprocs = 1
        self._autostart = False            #True/False
        self._autorestart = False          #True/False/"unexpected"
        self._stdout = "discard"           #[Path] or "discard"
        self._stderr = "discard"           #[Path] or "discard"
        self._workingdir = "/tmp"          #[Path]
        self._stopsignal = signal.SIGTERM  #def: SIGTERM
        self._env = os.environ             #True or False, if False: None
        self._exitcode = 0           
        self._starttime = 0            
        self._startretries = 2              
        self._stoptime = 10
        self._umask = 0o644               

        #Internal values
        self._start_status = "NotStarted"   #"NotStarted" or "Running" or "Exited"
        self._stdout_fd = None
        self._stderr_fd = None
        self._pid = None

def deci_to_octal(nb):
    ret = nb % 10
    nb = nb // 10
    i = 8
    while nb:
        target = nb % 10
        nb = nb // 10
        target *= i
        ret += target
        i *= 8
    return ret

def get_signum(subvalue):
    sigset = {"TERM": signal.SIGTERM,
              "QUIT": signal.SIGINT,
              "INT": signal.SIGINT}
    for key in sigset:
        if subvalue == key:
            return sigset[key]

def create_configured_programs(encoded_config):
    import sys

    raw_yaml = yaml.safe_load(encoded_config.decode())
    programs = list()
    for key, value in raw_yaml["program"].items():
        try:
            amt = value["numprocs"] 
        except KeyError:
            amt = 1
        for i in range(amt):
            if amt == 1:
                program_name = key
            else:
                program_name = key + ":" + str(i + 1)
            programs.append(Program(program_name, value["cmd"].split()))
            for subkey, subvalue in value.items():
                if subkey == "numprocs":
                    programs[-1]._numprocs = subvalue
                elif subkey == "stdout":
                    programs[-1]._stdout = subvalue
                elif subkey == "stderr":
                    programs[-1]._stderr = subvalue
                elif subkey == "autostart":
                    programs[-1]._autostart = subvalue
                elif subkey == "exitcode":
                    programs[-1]._exitcode = subvalue
                elif subkey == "starttime":
                    programs[-1]._starttime = subvalue
                elif subkey == "startretries":
                    programs[-1]._startretries = subvalue
                elif subkey == "stopsignal":
                    programs[-1]._stopsignal = get_signum(subvalue)
                elif subkey == "stoptime":
                    programs[-1]._stoptime = subvalue
                elif subkey == "env":
                    if type(subvalue) is dict:
                        new_env = deepcopy(os.environ)
                        for item in subvalue:
                            new_env[item] = subvalue[item]
                        programs[-1]._env = new_env
                elif subkey == "workingdir":
                    programs[-1]._workingdir = subvalue
                elif subkey == "umask":
                    if subvalue < 64:
                        programs[-1]._umask = subvalue
                    else:
                        programs[-1]._umask = deci_to_octal(subvalue)
                elif subkey == "autorestart":
                    programs[-1]._autorestart = subvalue
    return programs