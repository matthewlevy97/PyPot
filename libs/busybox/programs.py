from fs import *
import sys

fileSystem = FileSystem()

class wget():
	def execute(self, opts=[]):
		pass

class cat():
	def execute(self, opts=[]):
		f = fileSystem.open(opts[0])
		if f.exists():
			sys.stdout.write(f.read() + '\r\n')
		else:
			sys.stderr.write('cat: %s: No such file or directory\r\n' % opts[0])

class touch():
	def execute(self, opts=[]):
		if len(opts) == 0:
			sys.stderr.write("touch: missing file operand\r\nTry 'touch --help' for more information.\r\n")
			return

class echo():
	def execute(self, opts=[]):
		s = ''
		for o in opts:
			s += o + ' '
		sys.stdout.write(s + '\r\n')

class ls():
	def execute(self, opts=[]):
		options = []
		path    = []
		for o in opts:
			if o[0] == '-':
				options.append(o)
			else:
				path.append(o)
		print options
		print path
		
		if path == []:
			path.append('')
		
		for p in path:
			for f in fileSystem.getFiles(p):
				sys.stdout.write('%s\t' % f)
			sys.stdout.write('\r\n')

class rm():
	def execute(self, opts=[]):
		if len(opts) == 0:
			sys.stderr.write("rm: missing operand\r\nTry 'rm --help' for more information.\r\n")
			return
		
		for o in opts:
			if o[0] == '-' or o[0] == '*' or o == '.' or o == '..':
				continue
			f = fileSystem.open(o)
			if not f.read():
				sys.stderr.write("rm: cannot remove '%s': No such file or directory\r\n" % o)
				break

class exit():
	def execute(self, opts=[]):
		pass

class cd():
	def execute(self, opts=[]):
		if len(opts) > 0:
			if not fileSystem.setCWD(opts[0]):
				sys.stderr.write("bash: cd: %s: No such file or directory" % opts[0])

class pwd():
	def execute(self, opts=[]):
		sys.stdout.write(fileSystem.getCWD() + '\r\n')

programs = {'wget': wget(), 'cat': cat(), 'touch': touch(), 'echo': echo(), 'ls': ls(), 'rm': rm(), 'exit': exit(), 'cd': cd(), 'pwd': pwd()}
