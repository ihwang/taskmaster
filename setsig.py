import signal

import startshell



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
        