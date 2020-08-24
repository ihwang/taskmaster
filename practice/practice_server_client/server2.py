import socket
import struct

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def run_server(host='127.0.0.1', port=7788):
    BUFF_SIZE = 1024
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()

        data = recv_one_message(conn).decode()
        print(data)

run_server()

