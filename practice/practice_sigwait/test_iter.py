import signal

foo = {"TERM": signal.SIGTERM,
       "QUIT": signal.SIGQUIT,
       "KILL": signal.SIGKILL,
       "INT": signal. SIGINT}

#foo = iter(foo)

for key in foo:
    print(foo[key])
