from telnetsrv.threaded import TelnetHandler, command
import SocketServer

class TelnetServerHandler(TelnetHandler):
	WELCOME = ''
	PROMPT  = 'busybox> '
	authNeedUser = True
	authNeedPass = True
	
	def session_start(self):
		pass		
	def session_end(self):
		pass
	
	def authCallback(self, username, password):
		print username
		print password
		#raise RuntimeError('Invalid Login')

class TelnetServer(SocketServer.TCPServer):
	allow_reuse_address = True
