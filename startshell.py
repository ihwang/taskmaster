import cmd
import signal
import subprocess
import threading
import os

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

    def redirect_stdout_stderr(self, program):
        for i in range(program._cmd_amt):
            if program._stdout == "discard":
                program._processes[i]._stdout_fd = subprocess.DEVNULL
            else:
                program._processes[i]._stdout_fd = open(program._stdout, "a",
                    encoding="utf-8")
                os.chmod(program._stdout, 0o644)
            if program._stderr == "discard":
                program._processes[i]._stderr_fd = subprocess.DEVNULL
            else:
                program._processes[i]._stderr_fd = open(program._stdout, "a",
                    encoding="utf-8")
                os.chmod(program._stderr, 0o644)

    def run_single_process(self, P, p):
        retry_count = 0
        temp_umask = os.umask(self.programs[P]._processes[p]._umask)
        while True:
            self.redirect_stdout_stderr(self.programs[P])
            os.umask(self.programs[P]._processes[p]._umask)
            self.programs[P]._processes[p]._pid.append\
                (subprocess.Popen(self.programs[P]._cmd,
                stdout=self.programs[P]._stdout_fd,
                stderr=self.programs[P]._stderr_fd,
                close_fds=False, cwd=self.programs[P]._wd,
                env=self.programs[P]._env))
            try:
                self.programs[P]._processes[p]._pid[-1].wait(self.programs[P]._running_time)
            except subprocess.TimeoutExpired:
                flag_timeout = True
                self.programs[P]._processes[p]._pid[-1].wait()
            else:
                flag_timeout = False
            if self.programs[P]._auto_restart == True:
                continue
            elif self.programs[P]._auto_restart == "unexpected":
                if retry_count < self.programs[P]._retry_time and \
                    (self.programs[P]._expected_exit != \
                        self.programs[P]._processes[p]._pid[-1].returncode or \
                        flag_timeout is False):
                    retry_count += 1
                    continue
            break
        os.umask(temp_umask)

    def single_program(self, idx_p):
        for i in range(self.programs[idx_p]._cmd_amt):
            self.programs[idx_p]._thread.append( \
                threading.Thread(target=self.run_single_process,
                name=self.programs[idx_p]._name,
                args=(idx_p, i),
                daemon=True))
            self.programs[idx_p]._thread[i].start()
        
    def emptyline(self):
        pass

    def auto_start(self):
        for p in self.programs:
            if p._auto_start is True:
                self.do_start(p._name)

    def do_exit(self, notused):
        'exit the taskmaster shell'
        exit(0)
        return 0

    def do_reload(self, notused):
        'update the configuration file to the changed'
        raw_yaml = get_check_raw_yaml()
        self.programs = creat_full_config(raw_yaml)

    def do_status(self, name):
        'status'
        pass

    def do_start(self, name):
        'start'
        idx_p = 0
        for p in self.programs:
            if p._name == name and p._start_status != "NotStarted":
                print("%(name)s has been already" %{"name": p._name}, end="")
                print(" started. Check \'status\' command or \'restart\' it.")
            elif p._name == name:
                self.single_program(idx_p)
                p._start_status = "Running"
            idx_p += 1

    def do_restart(self, name):
        'restart'
        pass

def start_shell(programs):
    tm_shell = Commands(programs)    
    tm_shell.auto_start()
    tm_shell.cmdloop()