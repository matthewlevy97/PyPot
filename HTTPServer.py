from SimpleHTTPServer import *
from time import strftime
import SocketServer

from database import databaseConnection

DEFAULT_HTTP_RESPONSE = '<h1>This page exists</h1>'

class HTTPHandlerServer(SimpleHTTPRequestHandler):
	def __init__(self, request, cli_addr, server):
		SimpleHTTPRequestHandler.__init__(self, request, cli_addr, server)
	def do_GET(self):
		self.__logRequest()
		response = self.__generateResponse()
		self.__sendResponse(response)
	def do_POST(self):
		self.__logRequest()
		response = self.__generateResponse()
		self.__sendResponse(response)
	
	def __logRequest(self):
		body = ''
		length = int(self.headers.getheader('content-length', 0))
		if length:
			body = self.rfile.read(length)
		
		databaseConnection.insertHTTPConnection(self.client_address[0], self.client_address[1], self.path, self.command, self.headers.getheader('user-agent'), body)
	
	def __generateResponse(self):
		responses = databaseConnection.getHTTPResponse(self.path, self.command)
		if len(responses) < 1:
			return DEFAULT_HTTP_RESPONSE
		return responses[0]
	
	def __sendResponse(self, response):
		self.send_response(200)
		self.send_header("Content-length", len(response))
		self.end_headers()
		self.wfile.write(response)

def createServer(port=80):
	return SocketServer.TCPServer(('', port), HTTPHandlerServer)

if __name__=='__main__':
	createServer(9999).serve_forever()
