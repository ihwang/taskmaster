#!/usr/bin/env python3

class Flight():
	def __init__(self, name):
		self.name = name
	
    def print_name(self):
        print(name)

	def get_name(self):
		print_name()
		return name

f = Flight("abc")
f.get_name()

