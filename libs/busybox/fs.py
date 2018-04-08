import hashlib
import json
import os

class FileSystem():
	HOME_DIR = '/'
	
	def __init__(self):
		self.reset()
	
	def reset(self):
		with open(os.path.dirname(os.path.abspath(__file__)) + '/fs.json', 'r') as f:
			self.__files = json.load(f)
		self.__cwd = []
	
	def __followPath(self, path):
		cwd = self.__files
		
		for d in path.split('/'):
			if not d: break
			if d not in cwd:
				return None
			if 'type' not in cwd[d] or cwd[d]['type'] != 'd':
				return None
			cwd = cwd[d]['subfolders']
		return cwd
	
	def __parsePath(self, path):
		cwd = []
		
		# Generate absolute path
		for d in path:
			if d == '..':
				if len(cwd) > 0:
					cwd.pop()
			elif d == '.':
				continue
			else:
				cwd.append(d)
		
		# Combine array to generate absolute path and return
		return '/'.join(cwd)
		
	def __getPath(self, path):
		# Check if path is relative or absolute
		if path and path[0] == '/':
			# Path is absolute
			path = self.__parsePath(path[1:].split('/'))
		else:
			# Path is relative
			path = self.__parsePath(self.__cwd + path.split('/'))
		return self.__followPath(path)
	
	def open(self, fileName):
		if fileName[0] == '/':
			fileName = fileName[1:]
		
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
		with open('mal_folder/' + fileName, 'w') as f:
			f.write(fileObj.getData())
		
		fileName = fileObj.getFilename()
		cwd = self.__getPath(fileObj.getPath())
		
		# Are we in a directory?
		if cwd == None:
			return False
		
		# Create the file if it does not exist
		if fileName not in cwd:
			cwd[fileName] = {'type': 'f', 'contents': ''}
		
		# If the file already exists and is a directory, don't do anything
		if cwd[fileName]['type'] != 'f':
			return False
		
		cwd[fileName]['contents'] = fileObj.getData()
		return True
	
	def setCWD(self, path):
		# Check if path is relative or absolute
		if path and path[0] == '/':
			# Path is absolute
			path = self.__parsePath(path[1:].split('/'))
		else:
			# Path is relative
			path = self.__parsePath(self.__cwd + path.split('/'))
		
		cwd = self.__files
		tmp = []
		for d in path.split('/'):
			if not d: break
			if d not in cwd:
				return False
			if 'subfolders' not in cwd[d] or 'type' not in cwd[d] or cwd[d]['type'] != 'd':
				return False
			
			tmp.append(d)
			cwd = cwd[d]['subfolders']
		self.__cwd = tmp
		return True
	def getCWD(self):
		return '/' + '/'.join(self.__cwd)
	
	# Returns files in current working directory
	def getFiles(self, path=''):
		return self.__getPath(path).keys()
	
	def __str__(self):
		return json.dumps(self.__files, indent=4)

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
	print fs.setCWD('/bin')
	print fs.getCWD()
