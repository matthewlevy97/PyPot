from program import *

@create_program('cp')
class cp(Program):
	@execution_function
	def execute(self, params):
		print 'execute cp'
	def help(self):
		print 'cp help'
