import logging as log

from log2 import *

class foo:
    def __init__(self):
        log.basicConfig(filename="./foo", level=log.DEBUG)
        log.info("HI?")

instance = foo()
func()