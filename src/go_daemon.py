import os

def go_daemon():
    pid = os.fork()
    if pid > 0:
        exit(0)
    os.chdir("/")
    os.setsid()
    os.umask(0)
    pid = os.fork()
    if pid > 0:
        exit(0)