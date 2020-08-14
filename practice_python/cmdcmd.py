import cmd

class MyCmd(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '(MyCmd)'

	def do_test(self, line):
		print('cmd test ' + line)

	def complete_test(self, text, line, begidx, endidx):
		""" auto complete of file name.
		"""
		line = line.split()
		if len(line) < 2:
			filename = ''
			path = './'
		else:
			path = line[1]
			if '/' in path:
				i = path.rfind('/')
				filename = path[i+1:]
				path = path[:i]
			else:
				filename = path
				path = './'

		ls = dircache.listdir(path)
		ls = ls[:] # for overwrite in annotate.
		dircache.annotate(path, ls)
		if filename == '':
			return ls
		else:
			return [f for f in ls if f.startswith(filename)]



if __name__ == '__main__':
	mycmd = MyCmd()
	mycmd.cmdloop()
