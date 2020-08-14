class Flight():
    def __init__(self, name):
        self.name = name
    
    def print_name(self):
        print(self.name)

    def get_name(self):
        print_name()
        return self.name

f = Flight("abc")
f.get_name()