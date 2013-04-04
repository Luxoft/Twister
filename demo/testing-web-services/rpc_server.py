
import math

# version: 2.001
import cherrypy
from cherrypy import _cptools

#

class Server(_cptools.XMLRPCController):

	@cherrypy.expose
	def __dir__(self):
		return ['echo', 'sum', 'dif', 'mul', 'div']

	@cherrypy.expose
	def echo(self, msg):
		print  'Echo: %s' % msg
		return 'Echo: %s' % msg

	@cherrypy.expose
	def sum(self, x, y):
		return x + y

	@cherrypy.expose
	def dif(self, x, y):
		return x - y

	@cherrypy.expose
	def mul(self, x, y):
		return x * y

	@cherrypy.expose
	def div(self, x, y):
		return float(x) / float(y)

#

if __name__ == "__main__":

	root = Server()

	conf = {'global': {
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 55001,
		'server.thread_pool': 5,
		'engine.autoreload.on': False,
		'log.screen': True,
			}
		}

	# Start !
	print 'Starting RPC server...'
	cherrypy.quickstart(root, '/', config=conf)
