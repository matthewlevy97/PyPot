from fs import *

fileSystem = FileSystem()

class Output():
	def __init__(self):
		self.__dataLog = ''
	def read(self):
		tmp = self.__dataLog
		self.__dataLog = ''
		return tmp
	def write(self, data):
		self.__dataLog += data

stdout = Output()
stderr = Output()

class wget():
	def execute(self, opts=[]):
		pass

class cat():
	def execute(self, opts=[]):
		f = fileSystem.open(opts[0])
		if f.exists():
			stdout.write(f.read())
		else:
			stderr.write('cat: %s: No such file or directory\r\n' % opts[0])

class touch():
	def execute(self, opts=[]):
		if len(opts) == 0:
			stderr.write("touch: missing file operand\r\nTry 'touch --help' for more information.\r\n")
			return

class echo():
	def execute(self, opts=[]):
		s = ''
		for o in opts:
			s += o + ' '
		stdout.write(s + '\r\n')

class ls():
	def execute(self, opts=[]):
		options = []
		path    = []
		for o in opts:
			if o[0] == '-':
				options.append(o)
			else:
				path.append(o)
		if path == []:
			path.append('')
		
		for p in path:
			for f in fileSystem.getFiles(p):
				stdout.write('%s\t' % f)
			stdout.write('\r\n')

class rm():
	def execute(self, opts=[]):
		if len(opts) == 0:
			stderr.write("rm: missing operand\r\nTry 'rm --help' for more information.\r\n")
			return
		
		for o in opts:
			if o[0] == '-' or o[0] == '*' or o == '.' or o == '..':
				continue
			f = fileSystem.open(o)
			if not f.read():
				stderr.write("rm: cannot remove '%s': No such file or directory\r\n" % o)
				break

class exit():
	def execute(self, opts=[]):
		pass

class cd():
	def execute(self, opts=[]):
		if len(opts) > 0:
			if not fileSystem.setCWD(opts[0]):
				stderr.write("bash: cd: %s: No such file or directory" % opts[0])
		else:
			# Move to home directory if nothing provided
			fileSystem.setCWD(fileSystem.HOME_DIR)

class pwd():
	def execute(self, opts=[]):
		stdout.write(fileSystem.getCWD() + '\r\n')

programs = {'wget': wget(), 'cat': cat(), 'touch': touch(), 'echo': echo(), 'ls': ls(), 'rm': rm(), 'exit': exit(), 'cd': cd(), 'pwd': pwd()}
