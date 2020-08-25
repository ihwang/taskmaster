# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:13 by tango             #+#    #+#              #
#    Updated: 2020/08/25 22:50:21 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import signal
import struct
import logging as log

from src.feedback import recvall, recv_one_message, send_one_message

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
        self._config = self._conn.recv(2048)
   