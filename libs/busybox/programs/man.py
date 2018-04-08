from program import *

@create_program('man')
class man(Program):
	@execution_function
	def execute(self, params):
		if len(params) > 0 and params[0] in programs:
			programs[params[0]].helpLong()
	def help(self):
		print 'man pages'
