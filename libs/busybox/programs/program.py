import glob
from fs import *

fileSystem = FileSystem()
programs   = {}

class Output():
	def __init__(self):
		self.__dataLog = ''
	def read(self):
		tmp = self.__dataLog
		self.__dataLog = ''
		return tmp
	def write(self, data):
		self.__dataLog += data
stdout = Output()
stderr = Output()

class Program():
	def execute(self, params):
		pass
	def help(self):
		pass
	def helpLong(self):
		self.help()

# Used to create a new program and add to list
def create_program(program_name):
	def wrapper(program):
		global programs
		programs[program_name] = program()
	return wrapper

# Ensure that functions only get valid param values
def execution_function(func):
	# s = self parameter
	def wrapper(s, params):
		if params == None or type(params) == list:
			func(s, params)
	return wrapper

# Import everything in programs directory
for prog in glob.glob('programs/*.py'):
	prog = prog.replace('/', '.').replace('.py', '')
	if prog == 'programs.__init__' or prog == 'programs.program': continue
	__import__(prog)
