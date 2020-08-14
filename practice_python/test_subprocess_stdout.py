import subprocess
import os

r, w = os.pipe()
p = subprocess.Popen("cat", stdin=subprocess.PIPE, stdout=w)
p.stdin.write(bytes("1234", encoding="utf-8")
os.read(r, 4)

