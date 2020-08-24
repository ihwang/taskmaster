#!/usr/bin/env python3

import sys

class Rectangle:
	count = 0

	def __init__(self, width, height):
		self.width = width
		self.height = height
		Rectangle.count += 1

	def calcArea(self):
		area = self.width * self.height
		return area

	@staticmethod
	def isSquare(rectWidth, rectHeight):
		return rectWidth == rectHeight

	@classmethod
	def printCount(cls):
		print(cls.count)
	
	def __add__(self, other):
		obj = Rectangle(self.width + other.width, self.height + other.height)
		return obj

r1 = Rectangle(10, 5)
r2 = Rectangle(20, 15)
r3 = r1 + r2
r1.printCount()
r2.printCount()
r3.printCount()



