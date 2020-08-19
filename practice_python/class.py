#!/usr/bin/env python3

class Flight():
	foo = []
	def __init__(self, name):
		self.name = name
		self.foo.append(1)
		self.foo.append(2)
		self.foo.append(3)

	def func(self, subfoo):
		print(subfoo)

	def get_name(self):
		self.func(self.foo[0])
		return self.name

f = Flight("abc")
f.get_name()

