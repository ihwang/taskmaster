import socket
import logging as log
import struct
import time

def recvall(conn, buflen):
    buf = b''
    while buflen:
        newbuf = conn.recv(buflen)
        if not newbuf: return None
        buf += newbuf
        buflen -= len(newbuf)
    return buf

def recv_one_message(conn):
    lenbuf = recvall(conn, 4)
    len_count, = struct.unpack('!I', lenbuf)
    data = recvall(conn, len_count).decode()
    return data

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack("!I", length))
    sock.sendall(data.encode())


def feedback_listener(sock):
    time.sleep(1)
    while True:
        data = recv_one_message(sock)
        if data == "feedback_start":
            information = recv_one_message(sock)
            print(information)