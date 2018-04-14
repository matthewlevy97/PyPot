# Configuration settings for the honeypot
configuration = {
	'information': {
		'version': 1.0,
		'creator': 'Matthew Levy'
	},
	'log_files': {
		'stderr': 'access.log',
		'stdout': '.debug.log'
	},
	'http_server': {
		'enable': True,
		'port': 9999,
		'threads': 15
	}
}
