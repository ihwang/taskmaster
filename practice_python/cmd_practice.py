import cmd

class my(cmd.Cmd):
    intro = "Hello"
    prompt = "(mdp)"

    def do_hello(self, arg):
        'print Hello'
        self.hello(arg)
    
    def do_name(self, arg):
        'print name'
        self.name()

    def hello(self, arg):
        print('Hello', arg)

    def name(self):
        print('weejiwon')

    def job(self):
        print('College student')

my().cmdloop()