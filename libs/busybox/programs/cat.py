from program import *

@create_program('cat')
class cat(Program):
	@execution_function
	def execute(self, params):
		if len(params) > 0:
			f = fileSystem.open(params[0])
			if f.exists():
				stdout.write(f.read())
			else:
				stderr.write('cat: %s: No such file or directory\r\n' % params[0])
		else:
			# Read from stdin
			pass
	def help(self):
		print 'cat help'
