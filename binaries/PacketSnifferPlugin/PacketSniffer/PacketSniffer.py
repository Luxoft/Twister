#!/usr/bin/env python

# version: 3.001
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

from rpyc import Service as rpycService
from rpyc import connect as rpycConnect
from rpyc.utils.helpers import BgServingThread as rpycBgServingThread
from uuid import uuid4
from time import sleep
from copy import deepcopy
from thread import allocate_lock
from scapy.all import Automaton, ATMT, TCP, bind_layers, Packet, NoPayload, Raw

#from PacketSnifferClasses import OpenFlow, CentralEngineObject

from sys import maxsize
from socket import gethostname, gethostbyname, socket, AF_INET, SOCK_DGRAM, inet_ntoa
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




class Sniffer(Automaton):
	"""
	Packet Sniffer Scapy Automaton
	"""

	def parse_args(self, user, epConfig, OFPort=None, iface=None):
		Automaton.parse_args(self)

		self.has_iface = None
		if iface:
			ifaces = all_interfaces()
			for _iface in ifaces:
				if iface in _iface:
					self.has_iface = True
					self.socket_kargs = {'iface': iface, }
			if not self.has_iface:
				self.has_iface = False
				print('PT debug: set iface error: no such device')

		self.PAUSED = False
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

		# CE / EP
		self.epConfig = epConfig
		self.ceTraffic = list(set([(ep['CE_IP'], ep['CE_PORT']) for ep in self.epConfig]))
		self.uid = uuid4()

		self.reinitRetries = 0
		self.reinitMaxRetries = 4

		#
		PacketSnifferService.sniffer = self

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
											packetHead['destination']['mac'])

		if self.filters.has_key('-port_src'):
			filterStatus = (self.filters['-port_src'] ==
									str(packetHead['source']['port']))

		if self.filters.has_key('-port_dst'):
			filterStatus = (self.filters['-port_dst'] ==
									str(packetHead['destination']['port']))

		if self.filters.has_key('-ip_src'):
			filterStatus = (self.filters['-ip_src'] ==
											packetHead['source']['ip'])

		if self.filters.has_key('-ip_dst'):
			filterStatus = (self.filters['-ip_dst'] ==
											packetHead['destination']['ip'])

		return filterStatus

	def registerCE(self, ce_list):
		"""  """

		print('PT: starting register..')

		registered = False
		for ce in ce_list:
			try:
				# Try to connect to CE!
				connection = rpycConnect(host=ce[0],
											port=int(ce[1]),
											service=PacketSnifferService,
											config={
												'allow_all_attrs': True,
												'allow_pickle': True,
												'allow_getattr': True,
												'allow_setattr': True,
												'allow_delattr': True})

				with PacketSnifferService.connectionsLock:
					if PacketSnifferService.connections.has_key(connection._config['connid']):
						PacketSnifferService.connections[connection._config['connid']].update([('host',
																	'{}:{}'.format(ce[0], ce[1])), ])

				# hello
				hello = connection.root.hello('sniffer')

				if not hello:
					print('PT warning: Could not send hello to central engine {}..'.format(ce))
					continue

				# authenticate
				authenticated = connection.root.login(self.username, 'EP')

				if not authenticated:
					print('PT warning: Could not authenticate to central engine {}..'.format(ce))
					continue

				rpycBgServingThread(connection)

				# create user if ep is not running
				#connection.root.list_eps()

				registered = True
				self.reinitRetries = 0

				print('PT info: Registered to central engine {}..'.format(ce))
			except Exception as e:
				print('PT warning: Central Engine is down .... [{0}]'.format(e))


		if not registered:
			if self.reinitRetries < self.reinitMaxRetries:
				print('PT debug: no central engines; will retry [{r}] ..'.format(r=self.reinitRetries))
				self.reinitRetries += 1
				sleep(2)

				self.registerCE(ce_list)
			else:
				raise self.END()

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

				#print('PT debug: packet head exception (ip): {ex}'.format(ex=e))
			try:
				source['port'] = packet.payload.payload.fields['sport']
				destination['port'] = packet.payload.payload.fields['dport']
			except Exception as e:
				source['port'] = 'None'
				destination['port'] = 'None'

				#print('PT debug: packet head exception (port): {ex}'.format(ex=e))
		except Exception as e:
			source['mac'] = 'None'
			destination['mac'] = 'None'

			#print('PT debug: packet head exception (mac): {ex}'.format(ex=e))

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

		print('|||| BEGIN ||||')

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
			'packet_source': str(packet),
		}
		data['packet_head'].update([('id', str(uuid4())), ])

		with PacketSnifferService.connectionsLock:
			for conn in PacketSnifferService.connections:
				if PacketSnifferService.connections[conn]:
					try:
						response = PacketSnifferService.connections[conn]['root'].run_plugin('PacketSnifferPlugin',
																		{'command': 'pushpkt',
																			'data': data})
						if (not isinstance(response, dict) or not response.has_key('status') or
							not response['status']['success']):
							print('PT debug: Push packet error: {}'.format(response))
					except Exception as e:
						print('PT debug: Push packet error: {}'.format(e))
						#pass

		raise self.WAITING()


	# END
	@ATMT.state(final=1)
	def END(self):
		"""  """

		print('|||| END ||||')


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
			client_addr = self._conn._config['connid']
			#client_addr = self._conn._config['endpoints'][1]
			with self.connectionsLock:
				self.connections.update([(client_addr, {'root': self._conn.root}), ])

			print('PT debug: Connected from `{}`.'.format(client_addr))
		except Exception as e:
			print('PT debug: Connect error: {er}'.format(er=e))


	def on_disconnect(self):
		"""  """

		try:
			client = None
			client_addr = self._conn._config['connid']
			#client_addr = self._conn._config['endpoints'][1]
			with self.connectionsLock:
				client = self.connections.pop(client_addr)

			print('PT debug: Disconnected from `{}`.'.format(client_addr))

			sleep(2)
			if self.sniffer and not self.connections:
				print('PT debug: no connections.. trying to re-register..')
				self.sniffer.registerCE(self.sniffer.ceTraffic)
			elif self.sniffer and client:
				print('PT debug: {} connection is down.. trying to re-register..'.format(client))
				client = client['host'].split(':')
				self.sniffer.registerCE([(client[0], client[1])])
		except Exception as e:
			print('PT debug: Disconnect error: {er}'.format(er=e))


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


	#def exposed_stop(self):
	#	"""  """
	#	##
	#	return True


	#def exposed_restart(self):
	#	"""  """
	#
	#	if not self.sniffer:
	#		return False
	#
	#	self.sniffer.stop()
	#	sleep(2)
	#	self.sniffer.runbg()
	#
	#	return True


	def exposed_set_filters(self, filters):
		"""  """

		if not self.sniffer:
			return False

		self.sniffer.filters = deepcopy(filters)

		return True

