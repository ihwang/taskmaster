import os

r, w = os.pipe()
os.write(r, bytes("1234", encoding="utf-8"))