import socket
import signal
import struct
import logging as log

BUFF_SIZE = 2048
port_file = "/tmp/.TM_port_server"
log_file = "/tmp/TM_log.txt"

class Server:
    def __init__(self):
        log.basicConfig(level=log.DEBUG,
                        format="[%(asctime)s][%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=log_file)
    
    def start(self):
        log.info("server: Taskmaster daemon server is started")
        self._sock = socket.socket()
        self._sock.bind(("127.0.0.1", 0))
        host, port = self._sock.getsockname()
        log.info("server: Server's port number %(portnb)s is binded", {"portnb": port})
        with open(port_file, "w", encoding="utf-8") as fd_port:
            fd_port.write(str(port))
        self.wait_for_connect()
    
    def wait_for_connect(self):
        self._sock.listen()
        self._conn, self._client_addr = self._sock.accept()
        log.info("server: A client %(addr)s is connected", {"addr": self._client_addr})
        self.get_config()
    
    def get_config(self):
        self._config = self._conn.recv(BUFF_SIZE)
    
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