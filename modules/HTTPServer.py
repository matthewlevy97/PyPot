from BaseHTTPServer import *
from time import strftime
import threading
import socket

from httpDatabase import databaseConnection

DEFAULT_HTTP_RESPONSE = '<h1>This page exists</h1>'

class HTTPHandler(BaseHTTPRequestHandler):
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
		length = int(self.headers.getheader('Content-Length', 0))
		if length:
			body = self.rfile.read(length)
		
		databaseConnection.insertHTTPConnection(self.client_address[0], self.client_address[1], self.path, self.command, self.headers.getheader('user-agent'), body)
	
	def __generateResponse(self):
		response = databaseConnection.getHTTPResponse(self.path, self.command)
		if not response:
			return DEFAULT_HTTP_RESPONSE
		return response
	
	def __sendResponse(self, response):
		self.send_response(200)
		self.send_header("Content-Length", len(response))
		self.end_headers()
		self.wfile.write(response)

def createServer(port=80, numberThreads=10):
	addr = ('', port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(addr)
	sock.listen(10)
	
	class HTTPThread(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			self.daemon = True
			self.start()
		def run(self):
			httpd = HTTPServer(addr, HTTPHandler, False)
			httpd.socket = sock
			httpd.server_bind = self.server_close = lambda self: None
			httpd.serve_forever()
	
	threads = [HTTPThread() for i in range(numberThreads)]
	databaseConnection.flushQueue()

if __name__=='__main__':
	createServer(port=9998, numberThreads=5)
