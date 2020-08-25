# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    status.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:19 by tango             #+#    #+#              #
#    Updated: 2020/08/26 01:49:12 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging as log

from src.feedback import recvall, recv_one_message, send_one_message

def send_status(programs, name, server):
    ever_found = False
    send_one_message(server._conn, "feedback_status")
    for p in programs:
        if name == p._name or len(name) == 0:
            ever_found = True
            send_one_message(server._conn, p._name)
            if p._pid == None:
                send_one_message(server._conn, "NoPidYet")
            else:
                send_one_message(server._conn, str(p._pid.pid))
            send_one_message(server._conn, p._start_status)
    send_one_message(server._conn, "end_loop")
    if ever_found == False:
        send_one_message(server._conn, "no_such_program")
        log.info("server: No such program(s)")
    else:
        send_one_message(server._conn, "end_status")
        log.info("server: Completed to send status")

