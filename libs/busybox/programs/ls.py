from program import *

@create_program('ls')
class ls(Program):
	@execution_function
	def execute(self, params):
		options = []
		path    = []
		for p in params:
			if p[0] == '-':
				options.append(p)
			else:
				path.append(p)
		if path == []:
			path.append('')
		for p in path:
			for f in fileSystem.getFiles(p):
				stdout.write('%s\t' % f)
			stdout.write('\r\n')
	def help(self):
		print 'ls help'
