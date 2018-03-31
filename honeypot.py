import os
import sys

from database import databaseConnection
from HTTPServer import createServer

# Setup the database
databaseConnection.createDatabase()

# Fork
pid = os.fork()
if pid == 0:
	# Setup outputing to log file
	fd = os.open(".debug.log", os.O_RDWR | os.O_CREAT | os.O_APPEND)
	fd2 = os.open("access.log", os.O_RDWR | os.O_CREAT | os.O_APPEND)
	os.close(1)
	os.close(2)
	os.dup2(fd, 1) #STDOUT
	os.dup2(fd2, 2) #STDERR
	
	# Start HTTP Server
	http_server = createServer(9999)
	http_server.serve_forever()
	
	sys.exit(0)

# Save PID
with open('honey.pid', 'w') as f:
	f.write('%d' % pid)

print "Started honeypot"
