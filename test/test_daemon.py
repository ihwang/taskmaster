import os
import sys

print(os.getpid())

pid = os.fork()
if pid > 0:
    exit(0)


print(os.getpid())
os.chdir("/")
os.setsid(os.getpid())
os.umask(0)

pid = os.fork()

if pid > 0:
    exit(0)
print(os.getpid())
print(os.getsid())


fd = open("/Users/tango/42/taskmaster/test/ffoo", "a", encoding="utf-8")
fd.write('HI?')
fd.write(str(os.getppid()))

