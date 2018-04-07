import sys
sys.path.append('libs/')

from modules.TelnetServer import *

server = TelnetServer(('0.0.0.0', 2223), TelnetServerHandler)
server.serve_forever()

