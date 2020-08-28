# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    go_daemon.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/25 03:25:06 by tango             #+#    #+#              #
#    Updated: 2020/08/27 01:45:33 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys

def go_daemon():
    pid = os.fork()
    if pid > 0:
        exit(0)
    os.chdir("/")
    os.setsid()
    os.umask(0)
    sys.stdout.flush()
    sys.stderr.flush()
    fd_stdin_stored = os.dup(sys.stdin.fileno())
    fd_stdout_stored = os.dup(sys.stdout.fileno())
    fd_stderr_stored = os.dup(sys.stderr.fileno())
    fd_devnull_stdin = open(os.devnull, "r")
    fd_devnull_stdout = open(os.devnull, "a+")
    fd_devnull_stderr = open(os.devnull, "a+")
    os.dup2(fd_devnull_stdin.fileno(), sys.stdin.fileno())
    os.dup2(fd_devnull_stdout.fileno(), sys.stdout.fileno())
    os.dup2(fd_devnull_stderr.fileno(), sys.stderr.fileno())
    pid = os.fork()
    if pid > 0:
        exit(0)
    return (fd_stdin_stored, fd_stdout_stored, fd_stderr_stored)