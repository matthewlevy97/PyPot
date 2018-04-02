import sqlite3

MAX_IP_ENTRIES = 15

class DatabaseConnector():
	def __init__(self, filename="db.db"):
		self.__conn = sqlite3.connect(filename)
	
	def createDatabase(self):
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
	
	def insertHTTPConnection(self, ip, port, path, method, user_agent, body=''):
		c = self.__conn.cursor()
		for row in self.__conn.execute("SELECT count(src_ip) FROM http_connections WHERE src_ip='?'", (ip)):
			if row[0] > MAX_IP_ENTRIES: return
		
		c.execute('''INSERT INTO http_connections
		(src_ip, src_port, path, method, user_agent, body)
		VALUES
		(?, ?, ?, ?, ?, ?)
		''', (ip, port, path, method, user_agent, body))
		self.__conn.commit()
	
	def getHTTPResponse(self, path, method):
		ret = []
		for row in self.__conn.execute('SELECT html_response FROM http_responses WHERE path like ? and method like ?', (path, method)):
			ret.append(row[0])
		return ret
	
databaseConnection = DatabaseConnector()

if __name__=='__main__':
	databaseConnection.createDatabase()
	print databaseConnection.getHTTPResponse('/', 'GET')
