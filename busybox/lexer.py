import shlex
from programs import programs, fileSystem

class Shell():
	def parse(self, cmd):
		self.__data = cmd
		self.__lex()
		self.__process()
	
	def __lex(self):
		self.__parsed = []
		self.__data = self.__data.replace('||', ';')
		for part1 in self.__data.split(';'):
			part1 = part1.strip()
			spl = []
			for part2 in part1.split('&&'):
				part2 = part2.strip()
				spl.append(shlex.split(part2))
			self.__parsed.append(spl)
	
	def __process(self):
		for statement in self.__parsed:
			for cmd in statement:
				if not self.__lookupCommand(cmd):
					# If the command failed
					break
	def __lookupCommand(self, cmd):
		if cmd[0] in programs:
			programs[cmd[0]].execute(cmd[1:])
			return True
		print '%s: command not found' % cmd[0]
		return False
					
		

if __name__ == '__main__':
	data = 'cat text.txt; ls -lah && rm -rf *; rm text.txt||rm text.zzz'
	print data
	shell = Shell()
	
	while True:
		shell.parse(raw_input('%s> ' % fileSystem.getCWD()))
