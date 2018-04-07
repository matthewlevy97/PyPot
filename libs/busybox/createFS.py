import json

fs = {}

def createDirectory(directory):
	if directory[0] == '/': directory = directory[1:]
	directory = directory.split('/')
	
	cwd = fs
	for d in directory:
		if d not in cwd:
			cwd[d] = {'type': 'd', 'subfolders': {}}
		cwd = cwd[d]['subfolders']

def createFile(fileName, data):
	if fileName[0] == '/': fileName = fileName[1:]
	fileName = fileName.split('/')
	
	path = fileName[:-1]
	fileName = fileName[len(fileName) - 1]
	
	cwd = fs
	for f in path:
		if f not in cwd:
			cwd[f] = {'type': 'd', 'subfolders': {}}
		cwd = cwd[f]['subfolders']
	cwd[fileName] = {'type': 'f', 'contents': data}

if __name__ == '__main__':
	createFile('/etc/passwd', 'root:x:0:0:root:/root:/bin/bash')
	createFile('/etc/apache2/config.cfg', 'test config file')
	
	with open('fs.json', 'w') as f:
		json.dump(fs, f)
	print json.dumps(fs, indent=4, sort_keys=True)
