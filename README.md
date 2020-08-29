# Welcome to taskmaster 👋
> Taskmaster is a task-management python script that is structured as a server daemon and client control shell. Made on the purpose of self-learning python.

##### Dependancy
- Python 3.8.0


##### Install
- No installation required

## Overview
![ezgif com-gif-maker](https://user-images.githubusercontent.com/47879168/91639615-de899d80-ea52-11ea-97fd-7a7f383206af.gif)

## Getting start
Launch server first
```sh
python taskmasterd.py
```
Launch ctrl-shell with a configuration file
```sh
python taskmasterctl.py config.yaml
```

## Example config
Unnecessary configs can be omitted and will be setting to default
```yaml
---
program:                # mandatory
  sleep:                # mandatory
    cmd: "sleep 10"                 # mandatory
    numprocs: 3                     # 1 by default
    umask: 022                      # (int) 022 by default
    workingdir: "/Users/tango/"     # "/tmp" by default
    autostart: False                # False by default
    autorestart: False              # True, False or "unexpected". False by default
    exitcode: 1                     # 0 by default
    startretries: 3                 # 2 by default
    starttime: 10                   # 0 by default
    stopsignal: "TERM"              # "TERM", "QUIT" or "INT". "TERM" by default
    stdout: "/tmp"                  # "/path/name" or "discard" by default
    stderr: "discard"               # same with stdout
    env:                            # 'key: value' format. environ by default
      foo1: "bar1"
      foo2: "bar2"
```

## Available commands
- `help`or`?`
- `start`
- `restart`
- `status`
- `stop`
- `reload`
- `setemail`
- `unsetemail`
- `exit`

## Author

👤 **ihwang**

* Github: [@ihwang](https://github.com/ihwang)
* LinkedIn: [@Intaek Hwang](https://www.linkedin.com/in/intaek-hwang-30161b196/)
