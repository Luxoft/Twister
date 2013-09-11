#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# version: 2.002
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


from os import getenv, makedirs
from os.path import exists

from binascii import a2b_base64
from ast import literal_eval

from copy import deepcopy
from time import time

from json import dumps
from scapy.all import Packet, NoPayload, wrpcap

from rpyc import Service as rpycService
from rpyc.utils.factory import connect as rpycConnect
from rpyc.utils.helpers import BgServingThread as rpycBgServingThread

try:
    from openflow.of_13.parse import of_message_parse
except Exception as e:
    of_message_parse = None
    print('WARNING: openflow lib not found')

import cherrypy

from thread import allocate_lock

from BasePlugin import BasePlugin




class Plugin(BasePlugin):
    """
    Packet Sniffer plugin.
    """

    def __init__(self, user, data):
        if not data:
            return False

        BasePlugin.__init__(self, user, data)

        # history list length, packets buffer size, query buffer size
        self.data['historyLength'] = (40000,
            int(self.data['historyLength']))[int(self.data['historyLength'])>0]
        self.data['packetsBuffer'] = (400,
            int(self.data['packetsBuffer']))[int(self.data['packetsBuffer'])>0]

        # plugin status, packets list, temporary path to save pcap files,
        # packets list index limit, registered sniffers
        self.status = 'paused'
        self.packets = list()
        self.packetsLock = allocate_lock()
        self.pcapPath = getenv('TWISTER_PATH') + '/tmp'
        if not exists(self.pcapPath):
            makedirs(self.pcapPath)
        self.packetsIndexLimit = (self.data['historyLength']
                                    - self.data['packetsBuffer'])
        self.filters = dict()
        self.sniffers = list()

        self.commands = {
            'simple': [
                'echo',
                'registersniff',
                'pause', 'resume',
                'restart', 'reset',
                'savepcap',
                'getfilters',
                'setfilters',
            ],
            'argumented': [
                'query', 'querypkt',
            ]
        }

        PluginService.plugin = self


    def run(self, args):
        args = {k: v[0] if isinstance(v, list) else v for k,v in args.iteritems()}

        # response structure
        response = {
            'status': {
                'success': True,
                'message': 'None', # error message
            },
            'type': 'reply', # reply type
            'state': self.status, # state of plugin
            'data': 'None', # response data
        }

        if (not args.has_key('command') or args['command'] not in
                self.commands['simple'] + self.commands['argumented']):

            response['status']['success'] = False
            response['status']['message'] = 'unknown command'

        elif (args['command'] in self.commands['argumented']
                and not args.has_key('data')):
            response['status']['success'] = False
            response['status']['message'] = 'no command data specified'

        # echo
        elif args['command'] == 'echo':
            #response['type'] = 'echo reply'
            response = self.status

        # registersniff
        elif args['command'] == 'registersniff':
            response['type'] = 'register sniff reply'

            try:
                connection = rpycConnect(cherrypy.request.headers['Remote-Addr'],
                                                    args['data'], PluginService)
                rpycBgServingThread(connection)
                connection.root.hello(self.status)
                self.sniffers.append(connection)
            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = 'register sniff error: {err}'.format(err=e)

        # get / set filters
        elif args['command'] == 'getfilters':
            #response['type'] = 'getfilters reply'

            response = self.filters
        elif args['command'] == 'setfilters':
            response['type'] = 'setfilters reply'

            try:
                if args.has_key('data'):
                    data = args['data'].split()
                    data = {data[i]: data[i+1] for i in range(0, len(data)-1, 2)}

                    self.filters = dict((k,str(v)) for k,v in data.iteritems() if v is not None)
                else:
                    self.filters = {}

                with self.packetsLock:
                    self.packets = []
                response['data'] = {'index': 0}

                for sniffer in self.sniffers:
                    try:
                        sniffer.root.set_filters(self.filters)
                    except Exception as e:
                        print('set filters error: {}'.format(e))

            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = 'set filters error: {err}'.format(err=e)

        # pause / resume
        elif args['command'] in ['pause', 'resume']:
            response['type'] = 'pause/resume reply'

            oldStatus = self.status

            self.status = ('paused', 'running')[args['command']=='resume']

            if not oldStatus == self.status:
                if self.status == 'paused':
                    for sniffer in self.sniffers:
                        try:
                            _response = sniffer.root.pause()
                            if not _response:
                                self.status = oldStatus
                                response['status']['success'] = False
                        except Exception as e:
                            print('pause / resume error: {}'.format(e))
                else:
                    for sniffer in self.sniffers:
                        try:
                            _response = sniffer.root.resume()
                            if not _response:
                                self.status = oldStatus
                                response['status']['success'] = False
                        except Exception as e:
                            print('pasue / resume error: {}'.format(e))

            response['state'] = self.status

        # restart
        elif args['command'] == 'restart':
            response['type'] = 'restart reply'

            for sniffer in self.sniffers:
                    try:
                        _response = sniffer.root.restart()
                        if not _response:
                            response['status']['success'] = False
                    except Exception as e:
                        print('restart error: {}'.format(e))

        # reset
        elif args['command'] == 'reset':
            response['type'] = 'reset reply'
            with self.packetsLock:
                self.packets = []

            response['data'] = {'index': 0}

        # # query / querypkt
        # """ query for packets command (you must supply data field
        # in argument dictionary which represents the index you left from
        # and you will recive a new index on reponse which you will use
        # for the next call of the function)
        # query for packet command (you must supply data field
        # in argument dictionary which represents the id of the packet) """
        elif args['command'] in ['query', 'querypkt']:
            with self.packetsLock:
                try:
                    try:
                        packetIndex = int(args['data'])
                        packet = deepcopy(self.packets[packetIndex])
                    except Exception, e:
                        packetIndex = None
                        packet = None

                    if not packetIndex == 0:
                        packetID = str(args['data'])
                        for _packet in self.packets:
                            if _packet['packet_head']['id'] == packetID:
                                packetIndex = self.packets.index(_packet)
                                packet = deepcopy(_packet)


                    if packetIndex is not None:
                        if args['command'] == 'query':
                            response['type'] = 'query reply'

                            queriedPackets = []
                            packetID = None
                            packetIndex += 1
                            for _packet in self.packets[packetIndex:packetIndex \
                                                        + self.data['packetsBuffer']]:
                                pk = deepcopy(_packet)
                                pk.pop('packet_source')
                                packetID = pk['packet_head']['id']
                                queriedPackets.append(dumps(pk, encoding='latin'))

                            response['data'] = {
                                'id': (args['data'], packetID)[packetID is not None],
                                'packets': queriedPackets
                            }

                        else:
                            #response['type'] = 'querypkt reply'

                            packet = dumps(packet['packet_dict'], encoding='latin')
                            response = packet    #response['data'] = packet
                    else:
                        response['status']['success'] = False
                        if self.packets:
                            response['status']['message'] = 'packet index unknown'
                        else:
                            response['status']['message'] = 'packets list empty'

                    del packet
                except Exception, e:
                    response['status']['success'] = False
                    response['status']['message'] = 'command data not valid: \
                                                        {err}'.format(err=e)

        # savepcap
        elif args['command'] == 'savepcap':
            response['type'] = 'savepcap reply'

            try:
                filePath = '{pcap_path}/{user}[{epoch_time}].pcap'.format(
                                    pcap_path=self.pcapPath,
                                    user=self.user,
                                    epoch_time=str(time()).replace('.', '|'))

                wrpcap(filePath, [p['packet_source'] for p in self.packets])

                response = filePath
            except Exception, e:
                response['status']['success'] = False
                response['status']['message'] = 'savepcap error: {err}'.format(err=e)

        else:
            response['status']['success'] = False
            response['status']['message'] = 'except'

        return response




class PluginService(rpycService):
    """  """

    plugin = None
    connections = dict()

    def on_connect(self):
        """  """

        self.connections.update([(str(self) , 6633), ])

        try:
            client_addr = self._conn._config['endpoints'][1]
            print('Connected from `{}`.'.format(client_addr))
        except Exception as e:
            #print('Connect error: {er}'.format(er=e))
            pass


    def on_disconnect(self):
        """  """

        self.connections.pop(str(self))
        self.plugin.sniffers.pop(self.plugin.sniffers.index(self._conn))
        try:
            client_addr = self._conn._config['endpoints'][1]
            print('Disconnected from `{ip}:{port}`.'.format(ip=client_addr[0], port=client_addr[1]))
        except Exception as e:
            #print('Disconnect error: {er}'.format(er=e))
            pass


    def exposed_set_ofp_port(self, port):
        """  """

        self.connections.update([(str(self) , port), ])


    def exposed_pushpkt(self, packet):
        """  """

        if not self.plugin:
            print('push packet error: no plugin')
            return False

        print('|||||||||||||||||||||||||||||||||||||||||||')
        print(self)
        print(dir(self))
        print(self._conn)
        print(dir(self._conn))
        print(self._conn.root)
        print(dir(self._conn.root))
        print(packet)
        print(dir(packet))
        print(type(packet))
        #p = deepcopy(packet)
        #print(p)
        #print(type(p))
        print('|||||||||||||||||||||||||||||||||||||||||||')

        if (self.connections.has_key(str(self))
            and self.connections[str(self)] in
            [packet['packet_head']['source']['port'], packet['packet_head']['destination']['port']]
            and of_message_parse):
            try:
                _packet = of_message_parse(str(packet['packet_source'].payload.payload.load))
                packet = _packet.show()
            except Exception as e:
                packet = self.packet_to_dict(packet['packet_source'])
        else:
            packet = self.packet_to_dict(packet['packet_source'])

        packet.update([('packet_dict' , packet), ])
        with self.plugin.packetsLock:
            self.plugin.packets.append(packet)

        if len(self.plugin.packets) >= self.packetsIndexLimit:
            del self.plugin.plugin.packets[:self.data['packetsBuffer']]

        return True


    def packet_to_dict(self, packet):
        """ Recursive function to parse packet and return dict """

        if isinstance(packet, Packet):
            _packet = packet.fields
            if not isinstance(packet.payload, NoPayload):
                _packet['payload'] = packet.payload

            return {packet.name: self.packet_to_dict(_packet)}

        elif isinstance(packet, dict):
            for k,v in packet.iteritems():
                packet[k] = self.packet_to_dict(v)

            return packet

        elif isinstance(packet, list):
            for v in packet:
                packet[packet.index(v)] = self.packet_to_dict(v)

        else:

            return packet








"""

#### plugins.xml config ####

<Plugin>
    <name>PacketSnifferPlugin</name>
    <jarfile>PacketSnifferPlugin.jar</jarfile>
    <pyfile>PacketSnifferPlugin.py</pyfile>
    <status>enabled</status>
    <property>
        <propname>historyLength</propname>
        <propvalue>4000</propvalue>
    </property>
    <property>
        <propname>packetsBuffer</propname>
        <propvalue>400</propvalue>
    </property>
</Plugin>

"""
