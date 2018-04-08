from program import *

@create_program('help')
class help(Program):
	@execution_function
	def execute(self, params):
		for prog in programs:
			programs[prog].help()
	def help(self):
		print 'display this help'
