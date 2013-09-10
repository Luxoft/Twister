#!/usr/bin/env python

# version: 2.004
#
# -*- coding: utf-8 -*-
#
# File: PacketSniffer.py ; This file is part of Twister.
#
# Copyright (C) 2012-2013 , Luxoft
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from binascii import b2a_base64

from xmlrpclib import ServerProxy
from rpyc import Service as rpycService
from rpyc.utils.server import ThreadedServer as rpycThreadedServer
from uuid import uuid4
from time import sleep
from thread import start_new_thread, allocate_lock
from scapy.all import Automaton, ATMT, TCP, bind_layers, Packet, NoPayload, Raw

#from PacketSnifferClasses import OpenFlow, CentralEngineObject

from sys import maxsize
from socket import gethostname, gethostbyname, socket, AF_INET, SOCK_DGRAM, inet_ntoa, create_connection
from fcntl import ioctl
from struct import unpack, pack
from array import array




def all_interfaces():
	"""  """

	is_64bits = maxsize > 2**32
	struct_size = 40 if is_64bits else 32
	sock = socket(AF_INET, SOCK_DGRAM)
	max_possible = 8 # initial value
	while True:
		bytes = max_possible * struct_size
		names = array('B', '\0' * bytes)
		outbytes = unpack('iL', ioctl(
			sock.fileno(),
			0x8912,  # SIOCGIFCONF
			pack('iL', bytes, names.buffer_info()[0])
		))[0]
		if outbytes == bytes:
			max_possible *= 2
		else:
			break
	namestr = names.tostring()
	return [(namestr[i:i+16].split('\0', 1)[0],
			 inet_ntoa(namestr[i+20:i+24]))
			for i in range(0, outbytes, struct_size)]


class PacketSniffer():
	"""  """

	def __init__(self, user, epConfig, OFPort=None, iface=None):
		"""  """

		self.rpycThreadedServer = None

		# port range
		minport, maxport = 4444, 4488

		self.clientPort = 4444

		# find firs free port in range ..
		while self.clientPort <= maxport:
			try:
				self.rpycThreadedServer = rpycThreadedServer(PacketSnifferService, port=self.clientPort)
				self.sniffer = Sniffer(user, epConfig, self.rpycThreadedServer, OFPort, iface)
				self.rpycThreadedServer.service.sniffer = self.sniffer
				break
			except Exception as e:
				print(e)
				print('Sniffer warning, the port `{}` is taken!'.format(self.clientPort))
				self.clientPort += 1

				if self.clientPort > maxport:
					print('Cound not find any free port in range {} - {} !'.format(minport, maxport))
					self.rpycThreadedServer = None
					self.sniffer = None
					self.clientPort = None


	def run(self):
		"""  """

		if not self.rpycThreadedServer:
			print('Error: server not started')

		print('Sniffer will start on : `0.0.0.0:{}`.'.format(self.clientPort))

		self.sniffer.runbg()
		try:
			self.rpycThreadedServer.start()
		except (KeyboardInterrupt, SystemExit):
			pass
		self.stop()


	def stop(self):
		"""  """

		print('Terminating..')

		self.sniffer.stop()
		self.rpycThreadedServer.close()

		print('Terminated.')




class Sniffer(Automaton):
	"""
	Packet Sniffer Scapy Automaton
	"""

	def parse_args(self, user, epConfig, rpycConn, OFPort=None, _iface=None):
		Automaton.parse_args(self)

		self.has_iface = None
		if _iface:
			ifaces = all_interfaces()
			for __iface in ifaces:
				if _iface in __iface:
					self.has_iface = True
					self.socket_kargs = {'iface': _iface, }
			if not self.has_iface:
				self.has_iface = False

				print 'PT debug: set iface error: no such device'

		self.PAUSED = True
		self.OFPort = (OFPort, 6633)[OFPort is None]

		# openflow packet model connect
		#bind_layers(TCP, OpenFlow, sport=self.OFPort)
		#bind_layers(TCP, OpenFlow, dport=self.OFPort)

		# packet filters
		self.filters = None

		# user
		self.username = user
		self.userip = gethostbyname(gethostname())
		self.userhost = gethostname()

		# rpyc server
		self.rpycConn = rpycConn

		# CE / EP
		self.epConfig = epConfig
		self.ceTraffic = list(set([(ep['CE_IP'], ep['CE_PORT']) for ep in self.epConfig]))
		self.uid = uuid4()

		self.reinitRetries = 0
		self.reinitMaxRetries = 4

	def master_filter(self, packet):
		"""  """

		packetHead = self.packet_head_parse(packet)

		# default filter: exclude CE traffic
		if ((packetHead['source']['ip'], str(packetHead['source']['port'])) in self.ceTraffic or
			(packetHead['destination']['ip'], str(packetHead['destination']['port'])) in self.ceTraffic):
			return False

		if not self.filters: return True

		filterStatus = True

		if self.filters.has_key('-proto'):
			pkt = packet
			protocols = []
			while not isinstance(pkt, NoPayload):
				protocols.append(pkt.name)
				pkt = pkt.payload

			filterStatus = self.filters['-proto'] in protocols

		if self.filters.has_key('-mac_src'):
			filterStatus = (self.filters['-mac_src'] ==
											packetHead['source']['mac'])

		if self.filters.has_key('-mac_dst'):
			filterStatus = (self.filters['-mac_dst'] ==
											self.packetHead['destination']['mac'])

		if self.filters.has_key('-port_src'):
			filterStatus = (self.filters['-port_src'] ==
									str(self.packetHead['source']['port']))

		if self.filters.has_key('-port_dst'):
			filterStatus = (self.filters['-port_dst'] ==
									str(self.packetHead['destination']['port']))

		if self.filters.has_key('-ip_src'):
			filterStatus = (self.filters['-ip_src'] ==
											self.packetHead['source']['ip'])

		if self.filters.has_key('-ip_dst'):
			filterStatus = (self.filters['-ip_dst'] ==
											self.packetHead['destination']['ip'])

		return filterStatus

	def registerCE(self, ce_list):
		"""  """

		print('PT: starting register..')

		# Try to ping status from CE!
		ceObjects = dict()
		for ce in ce_list:
			try:
				create_connection((ce[0], ce[1]), 2)
				ceObjects.update([('{ip}:{port}'.format(ip=ce[0], port=ce[1]),
								ServerProxy('http://{us}:EP@{ip}:{port}/'.format(us=self.username,
																		ip=ce[0], port=ce[1]))), ])
				self.reinitRetries = 0
			except Exception as e:
				print 'PT warning: Central Engine is down .... [{0}]'.format(e)

		if not ceObjects:
			if self.reinitRetries < self.reinitMaxRetries:
				print 'PT debug: no central engines; will retry [{r}] ..'.format(r=self.reinitRetries)
				self.reinitRetries += 1
				sleep(2)

				self.registerCE(self.ceTraffic)
			else:
				raise self.END()

		args = {
			'command': 'registersniff',
			'data': self.rpycConn.port
		}

		registered = False
		try:
			for ce in ceObjects:
				# create user if ep is not running
				ceObjects[ce].getExecStatusAll(self.username)

				pluginData = ceObjects[ce].runPlugin(self.username, 'PacketSnifferPlugin', args)

				if not isinstance(pluginData, dict):
					print('PT debug: {}'.format(pluginData))

				if pluginData['status']['success']:
					registered = True
					print('registered to central engine {}..'.format(ce))
				else:
					print('could not register to central engine {}..'.format(ce))
					print(pluginData['status']['message'])
		except Exception as e:
			print 'PT debug: register CE {err}'.format(err=e)
			return False

		if not registered:
			return False

		print('PT: register end.')

		return True

	def packet_head_parse(self, packet):
		"""  """

		source = {}
		destination = {}
		try:
			source['mac'] = packet.fields['src']
			destination['mac'] = packet.fields['dst']

			try:
				source['ip'] = packet.payload.fields['src']
				destination['ip'] = packet.payload.fields['dst']
			except Exception as e:
				source['ip'] = 'None'
				destination['ip'] = 'None'

				#print 'PT debug: packet head exception (ip): {ex}'.format(ex=e)
			try:
				source['port'] = packet.payload.payload.fields['sport']
				destination['port'] = packet.payload.payload.fields['dport']
			except Exception as e:
				source['port'] = 'None'
				destination['port'] = 'None'

				#print 'PT debug: packet head exception (port): {ex}'.format(ex=e)
		except Exception as e:
			source['mac'] = 'None'
			destination['mac'] = 'None'

			#print 'PT debug: packet head exception (mac): {ex}'.format(ex=e)

		data = {
			'protocol': packet.payload.payload.name,
			'source': source,
			'destination': destination,
		}

		return data


	# BEGIN
	@ATMT.state(initial=1)
	def BEGIN(self):
		"""  """

		print '|||| BEGIN ||||'

		while not self.rpycConn.active:
			sleep(0.8)

		response = self.registerCE(self.ceTraffic)
		if not response:
			raise self.END()

		raise self.WAITING()


	# WAITING
	@ATMT.state()
	def WAITING(self):
		"""  """

		pass


	# RECEIVING
	@ATMT.receive_condition(WAITING)
	def receive_data(self, pkt):
		"""  """

		if self.has_iface is not None and not self.has_iface:
			raise self.WAITING()

		raise (self.RECEIVING(pkt), self.WAITING())[self.PAUSED]


	# RECEIVED
	@ATMT.state()
	def RECEIVING(self, packet):
		"""  """

		data = {
			'sniffer': {
				'ip': self.userip,
				'hostname': self.userhost,
				'username': self.username,
			},
			'packet_head': self.packet_head_parse(packet),
			'packet_source': packet,
		}
		data['packet_head'].update([('id', str(uuid4())), ])

		with self.rpycConn.service.connectionsLock:
			for conn in self.rpycConn.service.connections:
				if self.rpycConn.service.connections[conn]:
					try:
						self.rpycConn.service.connections[conn].pushpkt(data)
					except Exception as e:
						print('error: {}'.format(e))
						#pass

		raise self.WAITING()


	# END
	@ATMT.state(final=1)
	def END(self):
		"""  """

		self.rpycConn.close()

		print '|||| END ||||'


	"""
	# EVENTS
	@ATMT.ioevent(BEGIN, name='commands')
	def transition(self, fd):
		print 'in trans'
		commands = ['start', 'pause', 'resume', 'restart', 'stop']

		command = fd.recv()

		if command in commands:
			print 'PT debug: got command {cmd}'.format(cmd=command)
			if command == 'start':
				self.PAUSED = False

			elif command == 'pause':
				self.PAUSED = True

			elif command == 'resume':
				self.PAUSED = False

			elif command == 'restart':

				self.restart()

				raise self.WAITING()

			elif command == 'stop':

				raise self.END()
	"""




class PacketSnifferService(rpycService):
	"""  """

	sniffer = None
	connections = dict()
	connectionsLock = allocate_lock()


	def on_connect(self):
		"""  """

		try:
			client_addr = self._conn._config['endpoints'][1]
			#client_addr = self._conn._config['connid'].split(':')
			with self.connectionsLock:
				self.connections.update([('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]), None), ])

			print('Connected from `{}`.'.format(client_addr))
		except Exception as e:
			print('Connect error: {er}'.format(er=e))


	def on_disconnect(self):
		"""  """

		try:
			client_addr = self._conn._config['endpoints'][1]
			#client_addr = self._conn._config['connid'].split(':')
			with self.connectionsLock:
				self.connections.pop('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]))

			print('Disconnected from `{ip}:{port}`.'.format(ip=client_addr[0], port=client_addr[1]))

			if self.sniffer:
				self.sniffer.registerCE([(client_addr[0], client_addr[1])])
		except Exception as e:
			print('Disconnect error: {er}'.format(er=e))

		if not self.connections and self.sniffer:
			self.sniffer.registerCE(self.sniffer.ceTraffic)


	def exposed_hello(self, status):
		"""  """

		try:
			client_addr = self._conn._config['endpoints'][1]
			#client_addr = self._conn._config['connid'].split(':')
			with self.connectionsLock:
				self.connections.update([
						('{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1]), self._conn.root), ])

			if status == 'running':
				self.exposed_start()

			#print(self.connections['{ip}:{port}'.format(ip=client_addr[0], port=client_addr[1])]._conn.root.pushpkt({'test': 1}))

			print('Hello from {}'.format(client_addr))
		except Exception as e:
			print('Hello error: {er}'.format(er=e))


	def exposed_start(self):
		"""  """

		if not self.sniffer:
			return False

		if not self.sniffer.PAUSED:
			return False

		self.sniffer.PAUSED = False
		print('PT debug: sniffer status chaged: running')

		return True


	def exposed_pause(self):
		"""  """

		if not self.sniffer:
			return False

		if self.sniffer.PAUSED:
			return False

		self.sniffer.PAUSED = True
		print('PT debug: sniffer status chaged: paused')

		return True


	def exposed_resume(self):
		"""  """

		if not self.sniffer:
			return False

		if not self.sniffer.PAUSED:
			return False

		self.sniffer.PAUSED = False
		print('PT debug: sniffer status chaged: running')

		return True


	def exposed_stop(self):
		"""  """
		##
		return True


	def exposed_restart(self):
		"""  """

		if not self.sniffer:
			return False

		self.sniffer.stop()
		sleep(2)
		self.sniffer.runbg()

		return True


	def exposed_set_filters(self, filters):
		"""  """

		if not self.sniffer:
			return False

		self.sniffer.filters = filters

		return True

