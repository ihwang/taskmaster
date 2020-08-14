import cmd
import signal
import subprocess

from taskmaster import get_check_raw_yaml
from setconfig import creat_full_config

"""
def sig_handler():
    pass

def set_signal(programs):
    for value in programs:
        if value._sig_for_stop == "SIGTERM":
            sig = signal.SIGTERM
        elif value._sig_for_stop == "SIGQUIT":
            sig = signal.SIGQUIT
        elif value._sig_for_stop == "SIGINT":
            sig = signal.SIGINT
        elif value._sig_for_stop == "SIGKILL":
            sig = signal.SIGKILL
            """
        
class Commands(cmd.Cmd):
    def __init__(self, programs):
        self.programs = programs
        cmd.Cmd.__init__(self)
        self.intro = "\nWelcome to Taskmaster. Try \'help\' or \'?\' to see the available commands"
        self.prompt = "Taskmaster$> "
        self.doc_header = "Availiable commands"
        cmd.Cmd.emptyline(self)

    def redirect_stdout_stderr(self, i):
        program = self.programs[i]
        if program._stdout == "discard":
            program._stdout_fd = subprocess.DEVNULL
        else:
            program._stdout_fd = open(program._stdout, mode="a",
            encoding="utf-8")
        if program._stderr == "discard":
            program._stderr_fd = subprocess.DEVNULL
        else:
            program._stderr_fd = open(program._stderr, mode="a",
            encoding="utf-8")

        #subprocess.Popen("ls", excutable="/bin/bash", stdout=fd or DEVNULL, close_fds=False, cwd=path, restore_signals=False)
    def run_command(self, i):
        program = self.programs[i]
        self.redirect_stdout_stderr(i)
        for count in range(0, program._cmd_amt):
            program._procs.append(subprocess.Popen(program._cmd,
                executable="/bin/bash", stdout=program._stdout_fd,
                stderr=program._stdout_fd, close_fds=False,
                cwd=program._pwd, env=program._env ,shell=True))
            program._stdout_fd.close()
            program._stderr_fd.close()

    def emptyline(self):
        pass

    def auto_start(self):
        for p in self.programs:
            if p._auto_start is True:
                self.do_start(p._name)

    def do_exit(self, notused):
        'exit the taskmaster shell'
        exit(0)

    def do_reload(self, notused):
        'update the configuration file to the changed'
        raw_yaml = get_check_raw_yaml()
        self.programs = creat_full_config(raw_yaml)

    def do_status(self, name):
        'status'
        pass

    def do_start(self, name):
        'start'
        i = 0
        for p in self.programs:
            if p._name == name and p._start_status is True:
                print("%(name)s has been already" %{"name": p._name}, end="")
                print(" started. Check \'status\' command or \'restart\' it.")
                return 1
            elif p._name == name:
                self.run_command(i)
            i += 1

    def do_restart(self, name):
        'restart'
        pass

def start_shell(programs):
    tm_shell = Commands(programs)    
    tm_shell.auto_start()
    tm_shell.cmdloop()