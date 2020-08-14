import sys
import os

class Program:
    def __init__(self, name, cmd):
       self._name = name
       self._cmd = cmd
       self._cmd_amt = 1
       self._auto_start = True
       self._auto_restart = "never"
       self._exit_code = 0
       self._start_time = 5
       self._retry_time = 3
       self._sig_for_stop = "SIGTERM"
       self._stdout = "discard"
       self._stdout_fd = None
       self._stderr = "discard"
       self._stderr_fd = None
       self._env = os.environ
       self._pwd = os.getcwd()
       self._umask = 0o644
       self._logging = None
       self._procs = []
       self._start_status = False

def check_valid_yaml(raw_yaml):
    if "program" not in raw_yaml:
        print("taskmaster: Wrong config \'program:\' sholud be preceedded", file=sys.stderr)
        return False
    elif raw_yaml["program"] == None:
        print("taskmaster: Specify one program at least under the \'program\'", file=sys.stderr)
        return False
    for key, value in raw_yaml["program"].items():
        if "cmd" not in value:
            print("taskmaster: the program \'", key, "\' needs a \'cmd\' to execute", sep="", file=sys.stderr)
            return False
    return True

def creat_full_config(raw_yaml):
    programs = []
    i = 0
    for key, value in raw_yaml["program"].items():
        programs.append(Program(key, value["cmd"]))
        for (subkey, subvalue) in value.items():
            if subkey == "cmd_amt":
                programs[i]._cmd_amt = subvalue
            elif subkey == "auto_start":
                programs[i]._auto_start = subvalue
            elif subkey == "auto_restart":
                programs[i]._auto_restart = subvalue
            elif subkey == "exit_cod":
                programs[i]._exit_code = subvalue
            elif subkey == "start_time":
                programs[i]._start_time = subvalue
            elif subkey == "retry_time":
                programs[i]._retry_time = subvalue
            elif subkey == "sig_for_stop":
                programs[i]._sig_for_stop = subvalue
            elif subkey == "stdout":
                programs[i]._stdout = subvalue
            elif subkey == "stderr":
                programs[i]._stderr = subvalue
            elif subkey == "env":
                programs[i]._env = subvalue
            elif subkey == "cwd":
                programs[i]._cwd = subvalue
            elif subkey == "umask":
                programs[i]._umask = subvalue
            elif subkey == "logging":
                programs[i]._logging = subvalue
        i += 1
    return programs

