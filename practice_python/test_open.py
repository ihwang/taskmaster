import os

fd = open("./foo.txt", mode="a", encoding="utf-8")
os.write(fd, "HI?")