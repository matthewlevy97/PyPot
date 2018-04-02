from config import config
import hashlib
import json

class FileSystem():
	def __init__(self):
		with open('fs.json', 'r') as f:
			self.__files = json.load(f)
		self.__cwd = []
	
	def __getPath(self, path):
		cwd = None
		for c in self.__cwd:
			cwd = self.__files[c]['subfolders']
		
		for d in path.split('/'):
			if d not in cwd:
				return None
			if 'type' not in cwd[d] or cwd[d]['type'] != 'd':
				return None
			cwd = cwd[d]['subfolders']
		return cwd
	
	def open(self, fileName):
		if fileName[0] == '/': fileName = fileName[1:]
		fileName = fileName.split('/')
		
		path = fileName[:-1]
		fileName = fileName[len(fileName) - 1]
		
		# Get path to file
		cwd = self.__getPath('/'.join(path))
		
		# Make sure path exists
		if cwd == None:
			return File(fileName)
		
		# Make sure file exists
		if fileName not in cwd:
			return File(fileName)
		
		# Make sure file is actually a file
		if cwd[fileName]['type'] != 'f':
			return File(fileName)
		
		# Return file
		return File(fileName, data=cwd[fileName]['contents'], path='/'.join(path))
	
	def save(self, fileObj):
		if fileObj.getData() == None: return
		
		m = hashlib.sha1()
		m.update(fileObj.getData())
		fileName = m.hexdigest()
		with open(config['SAVE_FILE_DIRECTORY'] + fileName, 'w') as f:
			f.write(fileObj.getData())
		
		fileName = fileObj.getFilename()
		cwd = self.__getPath(fileObj.getPath())
		if cwd == None:
			return False
		
		if fileName not in cwd or cwd[fileName]['type'] != 'f':
			return False
		
		cwd[fileName]['contents'] = fileObj.getData()
		return True
		
	def setCWD(self, cwd):
		tmp = cwd
		if cwd[0] == '/':
			cwd = cwd[1:]
			tmp = fs
		
		for d in cwd.split('/'):
			self.__cwd.append(d)
		
	def getCWD(self):
		return '/' + '/'.join(self.__cwd)

class File():
	def __init__(self, fileName, data=None, path=''):
		self.__fileName = fileName
		self.__data = data
		self.__path = path
	def exists(self):
		if self.__data == None:
			return False
		return True
	def read(self, amount=-1):
		if self.__data == None: return ''
		if amount < 0: return self.__data
		return self.__data[:amount]
	def write(self, data, overwrite=True):
		if self.__data == None: self.__data = ''
		self.__data = data + (self.__data[len(data):] if overwrite else self.__data)
	def append(self, data):
		if self.__data == None: self.__data = ''
		self.__data += data
	
	def getFilename(self): return self.__fileName
	def getData(self): return self.__data
	def getPath(self): return self.__path
		
	def __str__(self):
		return self.__fileName

if __name__ == '__main__':
	fs = FileSystem()
	print fs.getCWD()
	fs.setCWD('/etc')
	print fs.getCWD()
	
	f = fs.open('passwd')
	print f.exists()
	print f.read()
