import signal
import subprocess
from time import sleep

def handler(signum, frame):
    sleep(1)
    print("1")
    sleep(1)
    print("2")
    sleep(1)
    print("3")
    sleep(1)
    print("4")
    sleep(1)
    print("5")
    sleep(1)
    print("6")

signal.signal(signal.SIGKILL, handler)

p = subprocess.run(["/bin/sleep", "20"])


while True:
    print("HI?")