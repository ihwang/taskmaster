# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    go_daemon.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:06 by tango             #+#    #+#              #
#    Updated: 2020/08/26 02:57:05 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

def go_daemon():
    pid = os.fork()
    if pid > 0:
        exit(0)
    os.chdir("/")
    os.setsid()
    os.umask(0)
    pid = os.fork()
    if pid > 0:
        exit(0)
   