from signal import *

for i in range(2, 9):
    print(i)
    signal(i, SIG_IGN)
for i in range(10, 16):
    print(i)
    signal(i, SIG_IGN)
if SIGINT == 2:
    print("HI")