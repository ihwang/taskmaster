# Welcome to taskmaster 👋
> Taskmaster is a process-management python script that is separated to server(daemon) and client control shell. This project led me to learn a new language(Python) and to write codes with the language at the same time. It was good practice for learning new stuff. In addition to that, I got practical usages of multi-threading, socket programming, and daemon process within making taskmaster.


<span style="color:grey">Note: Some of text-editing would possibly not work on gnome-terminal emulator</span>.

#### Dependancy
- Python 3.8.0

#### Install
- No installation or external library required

## Overview
![ezgif com-gif-maker](https://user-images.githubusercontent.com/47879168/91639615-de899d80-ea52-11ea-97fd-7a7f383206af.gif)
![ezgif com-crop](https://user-images.githubusercontent.com/47879168/91639657-1690e080-ea53-11ea-9137-06fb5fe52464.gif)
![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/47879168/91639668-2c060a80-ea53-11ea-9542-d1e33efd30ac.gif)

## Getting started
Launch server first
```sh
python taskmasterd.py
```
Launch ctrl-shell with a configuration file
```sh
python taskmasterctl.py config.yaml
```
Set an email address to get informed about the result of your process
```sh
setemail
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
    stdout: "/tmp/sleep_stdout"     # "/path/name" or "discard" by default
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
* LinkedIn: [@Intaek Hwang](https://www.linkedin.com/in/intaek/)
