# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    feedback.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:02 by tango             #+#    #+#              #
#    Updated: 2020/08/26 20:09:58 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import logging as log
import struct
import sys
import time
import os

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

def feedback_start(sock):
    information = recv_one_message(sock)
    print(information, file=sys.stderr)

def feedback_status(sock):
    i = 0
    while True:
        name = recv_one_message(sock)
        if name == "end_loop":
            break
        pid = recv_one_message(sock)
        status = recv_one_message(sock)
        if i == 0:
            print("program                 PID                 status")
            print("--------------------------------------------------")
        print("{0:<24s}".format(name), end="")
        print("{0:<20s}".format(pid), end="")
        print(status)
        i += 1
    result = recv_one_message(sock)
    if result == "no_such_program":
        print("No such program", file=sys.stderr)

def feedback_restart(sock):
    information = recv_one_message(sock)
    print(information, file=sys.stderr)

def feedback_stop(sock):
    information = recv_one_message(sock)
    print(information, file=sys.stderr)


def feedback_listener(sock):
    time.sleep(1)
    while True:
        job = recv_one_message(sock)
        if job == "feedback_start":
            feedback_start(sock)
        elif job == "feedback_status":
            feedback_status(sock)
        elif job == "feedback_restart":
            feedback_restart(sock)
        elif job == "feedback_stop":
            feedback_stop(sock)
        elif job == "disconnect":
            log.info("client: the server is down")
            os._exit(os.EX_NOHOST)