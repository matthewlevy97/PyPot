import os
import sys

# Add paths for easy imports
sys.path.append(sys.path[0] + '/libs/')
sys.path.append(sys.path[0] + '/modules/')

from config import configuration
from database import databaseConnection
from modules.HTTPServer import createServer as createHTTPServer
from modules.TelnetServer import createServer as createTelnetServer

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
		http_threads = createHTTPServer(port=configuration['http_server']['port'], numberThreads=configuration['http_server']['threads'])
		# Cleanup
		for thread in http_threads:
			thread.join()
		sys.exit(0)
	
	if configuration['telnet_server']['enable'] and os.fork() == 0:
		# Start Telnet Server
		telnet_server = createTelnetServer(port=configuration['telnet_server']['port'])
		sys.exit(0)
	
	import time
	while True:
		time.sleep(1)
		databaseConnection.flushQueues()
	sys.exit(0)
	
print "Starting PyPot (v %f)" % configuration['information']['version']
print "Created by %s" % configuration['information']['creator']
