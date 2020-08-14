class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def greeting(self):
        print('hi, Im {0}.'.format(self.name))
