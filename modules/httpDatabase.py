from Queue import Queue
import sqlite3
import thread

from config import configuration

class DatabaseConnector():
	def __init__(self, filename="honeycomb.db"):
		self.__filename = filename
		self.__httpConnectionQueue = Queue()
		self.__connect()
		self.__getHTTPResponses()
	
	def __connect(self):
		self.__conn = sqlite3.connect(self.__filename)
		self.__createDatabase()
	
	########### NON-THREAD SAFE METHODS ##############
	def __createDatabase(self):
		c = self.__conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS http_connections (
			src_ip text not null,
			src_port int not null,
			path text not null,
			method text not null,
			user_agent text not null,
			body text,
			date timestamp default current_timestamp
		)''')
		c.execute('''CREATE TABLE IF NOT EXISTS http_responses (
			path text not null,
			method text not null,
			html_response text not null,
			PRIMARY KEY (path, method)
		)''')
		self.__conn.commit()
		
	def __getHTTPResponses(self):
		self.__httpResponses = []
		for row in self.__conn.execute('SELECT * FROM http_responses'):
			self.__httpResponses.append({
				'path': row[0],
				'method': row[1],
				'html_response': row[2]
			})
	
	def flushQueue(self):
		import time
		c = self.__conn.cursor()
		while True:
			time.sleep(1)
			data = self.__httpConnectionQueue.get()
			while data:
				c.execute('''INSERT INTO http_connections
				(src_ip, src_port, path, method, user_agent, body)
				VALUES
				(?, ?, ?, ?, ?, ?)
				''', (data['ip'], data['port'], data['path'], data['method'], data['user_agent'], data['body']))
				try:
					data = self.__httpConnectionQueue.get(block=False)
				except:
					break
			self.__conn.commit()
	
	############### THREAD SAFE METHODS #################
	def insertHTTPConnection(self, ip, port, path, method, user_agent, body=''):
		self.__httpConnectionQueue.put({'ip': ip, 'port': port, 'path': path, 'method': method, 'user_agent': user_agent, 'body': body})
	
	def getHTTPResponse(self, path, method):
		ret = None
		for entry in self.__httpResponses:
			if entry['path'] == path and entry['method'] == method:
				self.__httpResponses.remove(entry)
				self.__httpResponses.insert(0, entry)
				ret = entry['html_response']
				break
		return ret

databaseConnection = DatabaseConnector()

if __name__=='__main__':
	databaseConnection.createDatabase()
	print databaseConnection.getHTTPResponse('/', 'GET')
