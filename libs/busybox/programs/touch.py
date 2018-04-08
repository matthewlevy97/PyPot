from program import *

@create_program('touch')
class touch(Program):
	@execution_function
	def execute(self, params):
		if len(params) == 1:
			f = fileSystem.open(params[0])
			fileSystem.save(f)
		else:
			stderr.write("touch: missing file operand\r\nTry 'touch --help' for more information.\r\n")
	def help(self):
		print 'touch help'
