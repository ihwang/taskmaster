import logging as log
import os
import subprocess
import time
import threading
import signal

from server import *
from programs import *
#from start import *

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
        pass

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
                log.info("server: The name of the program should be executed is %(pn)s, %(n)s", {"pn": p._name, "n": name})
                ever_started = True
                threading.Thread(target=self.run_program, args=(p,), daemon=True).start()
        if ever_started is False:
            log.info("server: Not able to find such program name")
            send_one_message(server._conn, "feedback_start")
            send_one_message(server._conn, "Not able to find such program name")

    def run_program(self, prog):
        retry_count = 0
        temp_umask = os.umask(prog._umask)

        while True:
            redirect_stdout_stderr(prog)
            os.umask(prog._umask)
            prog._pid = subprocess.Popen(prog._cmd,
                                stdout=prog._stdout_fd,
                                stderr=prog._stderr_fd,
                                close_fds=False,
                                cwd=prog._workingdir,
                                env=prog._env)
            prog._start_status = "Running"
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

    def restart(self, name, server):
        pass

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
                log.info("server: %(n)s has been requested to be started by a command", {"n": name})
                self.start(name, server)
            elif job == "restart":
                self.restart(name, server)

def redirect_stdout_stderr(program):
    if program._stdout == "discard":
        program._stdout_fd = subprocess.DEVNULL
    else:
        program._stdout_fd = open(program._stdout, "a", encoding="utf-8")
        os.chmod(program._stdout, 0o644)
    if program._stderr == "discard":
        program._stderr_fd = subprocess.DEVNULL
    else:
        program._stderr_fd = open(program._stderr, "a", encoding="utf-8")
        os.chmod(program._stderr, 0o644)
