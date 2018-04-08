from program import *

@create_program('cd')
class cd(Program):
	@execution_function
	def execute(self, params):
		if len(params) > 0:
			if not fileSystem.setCWD(params[0]):
				stderr.write("bash: cd: %s: No such file or directory" % params[0])
		else:
			fileSystem.setCWD(fileSystem.HOME_DIR)
	def help(self):
		print 'cd help'
