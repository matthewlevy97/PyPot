from program import *

@create_program('echo')
class echo(Program):
	@execution_function
	def execute(self, params):
		s = ''
		for p in params:
			s += p + ' '
		stdout.write(s + '\r\n')
	def help(self):
		print 'echo help'
