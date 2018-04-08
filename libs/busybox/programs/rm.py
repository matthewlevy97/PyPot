from program import *

@create_program('rm')
class rm(Program):
	@execution_function
	def execute(self, params):
		if len(params) > 0:
			for p in params:
				f = fileSystem.open(p)
				if not f.exists():
					stderr.write("rm: cannot remove '%s': No such file or directory\r\n" % p)
					break
		else:
			stderr.write("rm: missing operand\r\nTry 'rm --help' for more information.\r\n")
		
	def help(self):
		print 'rm help'
