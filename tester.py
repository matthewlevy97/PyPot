'''
Used to test out development features
Currently used to run the telnet server
'''

import sys
sys.path.append(sys.path[0] + '/libs/')

from modules.TelnetServer import *

server = TelnetServer(('0.0.0.0', 2223), TelnetServerHandler)
server.serve_forever()

