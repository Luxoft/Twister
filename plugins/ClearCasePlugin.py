#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# version: 1.000
#
# File: PacketSnifferPlugin.py ; This file is part of Twister.
#
# Copyright (C) 2012 , Luxoft
#
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


from BasePlugin import BasePlugin

from json import dumps as jsonDump


try:
	import cleartool
except Exception as e:
	raise e




class Plugin(BasePlugin):
	"""  """

	def __init__(self, user, data):
		"""  """

		if not data:
			return False

		BasePlugin.__init__(self, user, data)

		self.user = user
		self.data = data


	def run(self, args):
		"""  """

		args = {k: v[0] if isinstance(v, list) else v for k,v in args.iteritems()}

		# response structure
		response = False

		if not args.has_key('command') or not isinstance(args['command'], str):
			return response

		_response = cleartool.cmd(args['command'])
		response = {
			'status': _response[0],
			'data': _response[1],
			'error': _response[2]
		}

		return jsonDump(response)




"""

#### plugins.xml config ####

<Plugin>
	<name>ClearCase</name>
	<jarfile>ClearCasePlugin.jar</jarfile>
	<pyfile>ClearCasePlugin.py</pyfile>
	<status>disabled</status>
</Plugin>

"""

