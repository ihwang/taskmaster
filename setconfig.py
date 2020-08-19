import sys
import os

class Program:
    def __init__(self, name, cmd):
        self._name = name
        self._cmd = cmd
        self._cmd_amt = 1
        self._auto_start = False            #True/False
        self._stdout = "discard"            #{Path}/"discard"
        self._stderr = "discard"            #{Path}/"discard"
        self._logging = None                #{Path}/None
        self._sig_for_stop = "SIGTERM"      #def SIGTERM
        self._umask = 0o644                 #def 0o644
        self._expected_exit = 0             #def 0
        self._running_time = 0              #def 0
        self._auto_restart = False          #True/False/"unexpected"
        self._retry_time = 2                #def 2
        self._wd = "/tmp"                   #{Path}
        self._env = os.environ              #True/False, if False: None
        self._stdout_fd = None
        self._stderr_fd = None

        #Internal values
        self._start_status = "NotStarted"   #"NotStarted"/"Running"/"Exited"
        self._thread = []
        self._processes = []

class Process:
    def __init__(self):
        self._pid = []
        self._process_status = "NotStarted" #"Not started"/"Running"/"Exited"


def spaces_in(raw_yaml):
    for key in raw_yaml["program"]:
        if ' ' in key:
            return key
    return False

def check_valid_yaml(raw_yaml):
    program_name = spaces_in(raw_yaml)
    if "program" not in raw_yaml:
        print("taskmaster: Wrong config \'program:\' sholud be preceedded", file=sys.stderr)
        return False
    elif program_name != False:
        print("A white space is not allowed in the program name \'", program_name,
            "\'", sep="", file=sys.stderr)
        return False
    elif raw_yaml["program"] == None:
        print("taskmaster: Specify one program at least under the \'program\'", file=sys.stderr)
        return False
    for key, value in raw_yaml["program"].items():
        if "cmd" not in value:
            print("taskmaster: the program \'", key, "\' needs a \'cmd\' to execute", sep="", file=sys.stderr)
            return False
    return True

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

# Todo
# Resolve stat_status and process_status when reload
def creat_full_config(raw_yaml):
    programs = []
    for key, value in raw_yaml["program"].items():
        programs.append(Program(key, value["cmd"].split()))
        for (subkey, subvalue) in value.items():
            if subkey == "cmd_amt":
                programs[-1]._cmd_amt = subvalue
            elif subkey == "stdout":
                programs[-1]._stdout = subvalue
            elif subkey == "stderr":
                programs[-1]._stderr = subvalue
            elif subkey == "auto_start":
                programs[-1]._auto_start = subvalue
            elif subkey == "expected_exit":
                programs[-1]._expected_exit = subvalue
            elif subkey == "running_time":
                programs[-1]._running_time = subvalue
            elif subkey == "retry_time":
                programs[-1]._retry_time = subvalue
            elif subkey == "sig_for_stop":
                programs[-1]._sig_for_stop = subvalue
            elif subkey == "env":
                if subvalue == False:
                    programs[-1]._env = None
            elif subkey == "working_dir":
                programs[-1]._wd = subvalue
            elif subkey == "umask":
                if subvalue < 64:
                    programs[-1]._umask = subvalue
                else:
                    programs[-1]._umask = deci_to_octal(subvalue)
            elif subkey == "logging":
                programs[-1]._logging = subvalue
            elif subkey == "auto_restart":
                programs[-1]._auto_restart = subvalue
        i = programs[-1]._cmd_amt
        while i:
            programs[-1]._processes.append(Process())
            i -= 1
    return programs

