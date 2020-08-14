# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    taskmaster.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ihwang <ihwang@student.hive.fi>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/12 13:42:58 by tango             #+#    #+#              #
#    Updated: 2020/08/14 00:15:20 by ihwang           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import yaml
import sys
import cmd

import setconfig
import startshell

def get_check_raw_yaml():
    with open(sys.argv[1], "rt") as stream:
        raw_yaml = yaml.safe_load(stream)
    if setconfig.check_valid_yaml(raw_yaml) == False:
        exit(1)
    return raw_yaml

def main():
    if len(sys.argv) != 2:
        print("taskmaster: Usage: taskmaster.py [configfile]", file=sys.stderr)
        exit(1)
    raw_yaml = get_check_raw_yaml()
    programs = setconfig.creat_full_config(raw_yaml)
    startshell.start_shell(programs)
    
if __name__ == "__main__":
    main()