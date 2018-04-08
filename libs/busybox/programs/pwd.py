from program import *

@create_program('pwd')
class pwd(Program):
	@execution_function
	def execute(self, params):
		stdout.write(fileSystem.getCWD() + '\r\n')
	def help(self):
		print 'pwd help'
