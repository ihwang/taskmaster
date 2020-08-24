import threading
import signal
import time

def foo():
    signals = list()
    signals.append(signal.SIGHUP)
    sigset = iter(signals)
    signal.sigwait(sigset)
    print("Got it!")

#signal.signal(signal.SIGHUP, signal.SIG_IGN)
#t = threading.Thread(target=foo).start()
threading.Thread(target=foo).start()

while True: pass

print("I die")