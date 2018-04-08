import sys
#from programs import programs, fileSystem, stdout, stderr
from programs.program import *

class Shell():
	ERROR   = False
	SUCCESS = True	
	
	FILE = 'file'
	CMD_OUTPUT = 'cmd_out'
	
	CMD = 'cmd'
	OR  = 'or'
	AND = 'and'
	
	def restart(self):
		fileSystem.reset()
	
	def parse(self, unparsedCMD):
		self.__data = unparsedCMD
		
		# Build statements
		parsed = []
		
		cmd = self.__generateCMD()
		parsed.append(cmd)
		
		getOutFileName = False
		getInFileName  = False
		for dat in self.__data:
			if not cmd['cmd']:
				cmd['cmd'] = dat
			else:
				# Parameter or statement seperator
				if dat == ';':
					getOutFileName = False
					getInFileName  = False
					if cmd['cmd']:
						cmd = self.__generateCMD()
						parsed.append(cmd)
				
				elif dat == '|':
					getOutFileName = False
					getInFileName  = False
					cmd['output'] = {'type': self.CMD_OUTPUT, 'out_cmd': self.__generateCMD()}
					cmd = cmd['output']['out_cmd']
					
				
				elif dat == '||':
					getOutFileName = False
					getInFileName  = False
				elif dat == '&&':
					getOutFileName = False
					getInFileName  = False
				
				elif getOutFileName:
					cmd['output']['fileName'] = dat
				elif getInFileName:
					cmd['input']['fileName']  = dat
				elif dat == '>':
					cmd['output'] = {'overwrite': True, 'type': self.FILE}
					getOutFileName = True
				elif dat == '>>':
					cmd['output'] = {'overwrite': False, 'type': self.FILE}
					getOutFileName = True
				elif dat == '<':
					getInFileName = True
				
				else:
					cmd['params'].append(dat)
		
		# Process statements
		return_output = {'stdout': '', 'stderr': ''}
		for statement in parsed:
			if statement['type'] == self.CMD:
				self.__lookupCommand(statement['cmd'], statement['params'])
				out = stdout.read()
				err = stderr.read()
				if statement['output']:
					if statement['output']['type'] == self.FILE:
						fileObj = fileSystem.open(statement['output']['fileName'])
						fileObj.write(out, overwrite=statement['output']['overwrite'])
						fileSystem.save(fileObj)
				else:
					return_output['stdout'] += out
					return_output['stderr'] += err
		if return_output['stdout'].endswith('\r\n'):
			return_output['stdout'] = return_output['stdout'][:-2]
		if return_output['stderr'].endswith('\r\n'):
			return_output['stderr'] = return_output['stderr'][:-2]
		return return_output
	
	def __generateCMD(self):
		return {'type': self.CMD, 'cmd': '', 'params': [], 'input': None, 'output': None}
	
	def __lookupCommand(self, cmd, params):
		if cmd in programs:
			return programs[cmd].execute(params)
		return None
					
		

if __name__ == '__main__':
	shell = Shell()
	while True:
		output = shell.parse(raw_input('%s> ' % fileSystem.getCWD()).split(' '))
		if output['stdout']:
			print output['stdout']
		if output['stderr']:
			print output['stderr']
