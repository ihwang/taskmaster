import socket
import struct

def send_one_message(sock, data):
    length = len(data)
    packed = struct.pack('!I', length)
    print(packed)
    sock.sendall(packed)
    sock.sendall(data.encode())



def run_client(host='127.0.0.1', port=7788):
    with socket.socket() as sock:
        sock.connect((host, port))

        data = "start"
        send_one_message(sock, data)

run_client()