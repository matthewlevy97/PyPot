import os
import sys

# Add paths for easy imports
sys.path.insert(0, sys.path[0] + '/modules/')

from config import configuration
from modules.HTTPServer import createServer as createHTTPServer

# Fork
pid = os.fork()
if pid == 0:
	# Setup outputing to log file
	fd = os.open(configuration['log_files']['stdout'], os.O_RDWR | os.O_CREAT | os.O_APPEND)
	fd2 = os.open(configuration['log_files']['stderr'], os.O_RDWR | os.O_CREAT | os.O_APPEND)
	os.dup2(fd, 1) #STDOUT
	os.dup2(fd2, 2) #STDERR
	
	if configuration['http_server']['enable'] and os.fork() == 0:
		# Start HTTP Server
		createHTTPServer(port=configuration['http_server']['port'], numberThreads=configuration['http_server']['threads'])
		sys.exit(0)
	
	sys.exit(0)
	
print "Starting PyPot (v %f)" % configuration['information']['version']
print "Created by %s" % configuration['information']['creator']
