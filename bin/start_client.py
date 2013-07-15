#!/usr/bin/python

# version: 1.000

# This file will register ALL Execution Processes that are enabled,
# from file `twister/config/epname.ini` !
# To be able to start the packet sniffer, this must run as ROOT.


import os, sys
import xmlrpclib
import subprocess

from time import sleep
from datetime import datetime
from ConfigParser import SafeConfigParser
from json import loads as jsonLoads, dumps as jsonDumps

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from thread import start_new_thread




if not sys.version.startswith('2.7'):
	print('Python version error! Execution Process must run on Python 2.7!')
	exit(1)

try:
	username = os.getenv('USER')
	if username=='root':
		username = os.getenv('SUDO_USER')
except:
	print('Cannot guess user name for this Execution Process! Exiting!')
	exit(1)


def userHome(user):
	""" return user home path for all kind of users """
	return subprocess.check_output('echo ~' + user, shell=True).strip()


# Twister path environment
os.environ['TWISTER_PATH'] = userHome(username) + '/twister'

#

def keepalive(service):
	"""  """

	print('CE keepalive started..')
	while True:
		for ce in service.proxyList:
			try:
				response = service.proxyList[ce].echo('ping')
			except Exception as e:
				print('PT warning: Central Engine is down .... [{0}]'.format(e))
				print('Enter register eps state..')
				service.registerEPs()
		sleep(0.8)


# restrict to a particular path.
class ServiceHandler(SimpleXMLRPCRequestHandler):
	"""  """

	rpc_paths = ('/twisterclient/',)


class TwisterClientService():
	"""  """

	def __init__(self, username):
		"""  """

		print('Twister Client Service init..')
		self.username = username

		# close sniffer and ep instaces and parse eps
		pipe = subprocess.Popen('ps ax | grep start_packet_sniffer.py', shell=True, stdout=subprocess.PIPE)
		for line in pipe.stdout.read().splitlines():
			try:
				os.kill(int(line.split()[0]), 9)
			except Exception as e:
				pass
		del pipe

		pipe = subprocess.Popen('ps ax | grep ExecutionProcess.py', shell=True, stdout=subprocess.PIPE)
		for line in pipe.stdout.read().splitlines():
			try:
				os.kill(int(line.split()[0]), 9)
			except Exception as e:
				pass
		del pipe


		cfg = SafeConfigParser()
		cfg.read(os.getenv('TWISTER_PATH') + '/config/epname.ini')

		# sniffer config
		self.snifferEth = None
		if cfg.get('PACKETSNIFFERPLUGIN', 'ENABLED') == '1':
			self.snifferEth = cfg.get('PACKETSNIFFERPLUGIN', 'ETH_INTERFACE')


		# All sections that have an option CE_IP, are EP names
		eps = [e for e in cfg.sections() if cfg.has_option(e, 'CE_IP')]
		print('Found `{}` EPs: `{}`.\n'.format(len(eps), ', '.join(eps)))

		# eps
		self.eps = dict()
		self.proxyList = dict()
		for currentEP in eps:
			newEP = dict()
			newEP['ce_ip'] = cfg.get(currentEP, 'CE_IP')
			newEP['ce_port'] = cfg.get(currentEP, 'CE_PORT')

			_proxy = '{ip}:{port}'.format(ip=newEP['ce_ip'], port=newEP['ce_port'])
			if self.proxyList.has_key(_proxy):
				newEP['proxy'] = self.proxyList[_proxy]
			else:
				newEP['proxy'] = xmlrpclib.ServerProxy('http://{0}:{1}/'.format(
														newEP['ce_ip'], newEP['ce_port']))
				self.proxyList.update([(_proxy, newEP['proxy']), ])

			newEP['exec_str'] = 'nohup {python} -u {twister_path}/client/executionprocess/ExecutionProcess.py '\
				'{user} {ep} "{ip}:{port}" {sniff} > "{twister_path}/.twister_cache/{ep}_LIVE.log" &'.format(
				python = sys.executable,
				twister_path = os.getenv('TWISTER_PATH'),
				user = self.username,
				ep = currentEP,
				ip = newEP['ce_ip'],
				port = newEP['ce_port'],
				sniff = self.snifferEth,
			)
			newEP['pid'] = None
			self.eps.update([(currentEP, newEP), ])


		# create server
		self.clientPort = 4444
		maximumServersNumber = 44
		serverEstablished = False
		while not serverEstablished or not self.clientPort > 4488:
			try:
				self.server = SimpleXMLRPCServer(("0.0.0.0", self.clientPort),
													requestHandler=ServiceHandler)
				self.server.register_introspection_functions()

				serverEstablished = True
				break
			except Exception as e:
				print('Twister Client Service Error: '\
						'could not bind {p} :: {er}'.format(er=e, p=self.clientPort))
				self.server = None
				self.clientPort += 1


	def registerEPs(self):
		""" register EP to CE """

		print('Twister Client Service register..')
		proxyEpsList = dict()
		for currentEP in self.eps:
			_proxy = '{ip}:{port}'.format(ip=self.eps[currentEP]['ce_ip'],
										port=self.eps[currentEP]['ce_port'])
			if not proxyEpsList.has_key(_proxy):
				proxyEpsList[_proxy] = [epname for epname in self.eps
									if self.eps[epname]['ce_ip'] == self.eps[currentEP]['ce_ip'] and
									self.eps[epname]['ce_port'] == self.eps[currentEP]['ce_port']]

		unregistered = True
		while unregistered:
			for currentCE in proxyEpsList:
				proxy = self.eps[proxyEpsList[currentCE][0]]['proxy']

				clientKey = ':{port}'.format(port=self.clientPort)
				try:
					userCeClientInfo = proxy.getUserVariable(self.username, 'clients')

					if not userCeClientInfo:
						userCeClientInfo = dict()
					else:
						userCeClientInfo = jsonLoads(userCeClientInfo)


					ceStatus = str()
					while not ceStatus.startswith('stopped'):
						ceStatus = proxy.getExecStatusAll(self.username)

						if ceStatus.startswith('stopped'):
							# reset user project
							proxy.resetProject(self.username)
							print('User project reset.')
						else:
							print('CE running: {}'.format(ceStatus))
							print('Waiting to stop..')
						sleep(2)

					userCeClientInfo.update([(clientKey, proxyEpsList[currentCE]), ])
					userCeClientInfo = jsonDumps(userCeClientInfo)

					proxy.registerClient(self.username, userCeClientInfo)

					unregistered = False
				except Exception as e:
					print('Error: {er}'.format(er=e))
			if unregistered:
				print('Error: CE down.. will retry..')
			sleep(2)

		print('Registered.')


	def startEP(self, epname):
		"""  """

		if not epname in self.eps.keys():
			print('Error: unknown ep name')
			return False

		sleep(2.4)
		try:
			last_seen_alive = self.eps[epname]['proxy'].getEpVariable(self.username,
															epname, 'last_seen_alive')
		except:
			print('Error: Cannot connect to Central Engine to check the EP!\n')
			return False

		now_dtime = datetime.today()

		if last_seen_alive:
			diff = now_dtime - datetime.strptime(last_seen_alive, '%Y-%m-%d %H:%M:%S')
			if diff.seconds < 2.5:
				print('Error: Process {0} is already started for user {1}! (ping={2} sec)\n'\
						.format(epname, username, diff.seconds))
				return False

		if self.eps[epname]['pid']:
			print('Error: Process {0} is already started for user {1}! (pid={2})\n'\
					.format(epname, username, self.eps[epname]['pid']))
			return False

		print('Will execute:', self.eps[epname]['exec_str'])
		self.eps[epname]['pid'] = subprocess.Popen(self.eps[epname]['exec_str'],
													shell=True, preexec_fn=os.setsid)
		print('Ok! `%s` for user `%s` launched in background!\n' % (epname, self.username))

		return True


	def stopEP(self, epname):
		"""  """

		if not epname in self.eps.keys():
			print('Error: unknown ep name')
			return False

		if not self.eps[epname]['pid']:
			print('Error: ep is not running')
			return False

		sleep(2.4)
		os.killpg(self.eps[epname]['pid'].pid, 9)
		self.eps[epname]['pid'] = None

		print('Received STOP EP {} !'.format(epname))
		return True


	def restartEP(self, epname):
		"""  """

		if not epname in self.eps.keys():
			print('Error: unknown ep name')
			return False

		if self.eps[epname]['pid']:
			os.killpg(self.eps[epname]['pid'].pid, 9)
			self.eps[epname]['pid'] = None
			print('Killing EP {} !'.format(epname))

		print('Will execute:', self.eps[epname]['exec_str'])
		self.eps[epname]['pid'] = subprocess.Popen(self.eps[epname]['exec_str'],
													shell=True, preexec_fn=os.setsid)
		print('Ok! RESTARTED! `%s` for user `%s` launched in background!\n' % (epname, self.username))

		return True




	def run(self):
		"""  """

		# register functions
		self.server.register_function(self.startEP, 'startEP')
		self.server.register_function(self.stopEP, 'stopEP')
		self.server.register_function(self.restartEP, 'restartEP')

		print('Twister Client Service start..')

		# run the server's main loop
		self.server.serve_forever()



if __name__ == "__main__":
	# run client service
	service = TwisterClientService(username)
	if not service.server:
		print('Could not establish server on any port! Exiting!')
		exit(1)

	service.registerEPs()
	start_new_thread(keepalive, (service, ))
	service.run()

