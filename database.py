from Queue import Queue
import sqlite3

from config import configuration

MAX_IP_ENTRIES = configuration['database']['max_repeat_ip_addresses']

class DatabaseConnector():
	def __init__(self, filename="honeycomb.db"):
		self.__httpConnectionQueue = Queue()
		self.__conn = sqlite3.connect(filename)
		self.__createDatabase()
		self.__getHTTPResponses()
	
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
	
	def flushQueues(self):
		data = self.__httpConnectionQueue.get()
		while data:
			c = self.__conn.cursor()
			for row in self.__conn.execute("SELECT count(src_ip) FROM http_connections WHERE src_ip='?'", (ip)):
				if row[0] > MAX_IP_ENTRIES: return
			
			c.execute('''INSERT INTO http_connections
			(src_ip, src_port, path, method, user_agent, body)
			VALUES
			(?, ?, ?, ?, ?, ?)
			''', (ip, port, path, method, user_agent, body))
			data = self.__httpConnectionQueue.get()
		self.__conn.commit()
	
	############### THREAD SAFE METHODS #################
	def insertHTTPConnection(self, ip, port, path, method, user_agent, body=''):
		self.__httpConnectionQueue.put({'ip': ip, 'port': port, 'method': method, 'user_agent': user_agent, 'body': body})
	
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
