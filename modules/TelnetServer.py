from telnetsrv.threaded import TelnetHandler, command
import SocketServer

class TelnetServerHandler(TelnetHandler):
	WELCOME = ''
	PROMPT  = 'busybox> '
	ERROR_MSG = 'Applet Unknown: %s'
	
	authNeedUser = True
	authNeedPass = True
	
	def authCallback(self, username, password):
		print "New Login: <%s:%s>" % (username, password)

class TelnetServer(SocketServer.TCPServer):
	allow_reuse_address = True
