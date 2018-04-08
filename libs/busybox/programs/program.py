import glob
import os
from busybox.fs import *

fileSystem = FileSystem()
programs = {}

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

def loader():
	# Import everything in programs directory
	program_dir = os.path.dirname(os.path.abspath(__file__)).replace(os.getcwd() + '/', '')
	for prog in glob.glob(program_dir + '/*.py'):
		prog = prog[prog.find('busybox/programs/'):].replace('/', '.').replace('.py', '')
		if prog.endswith('__init__') or prog.endswith('.program'): continue
		__import__(prog)
