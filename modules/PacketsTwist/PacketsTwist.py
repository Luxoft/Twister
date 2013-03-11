#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
#
# File: PacketsTwist.py ; This file is part of Twister.
#
# Copyright (C) 2012 , Luxoft
#
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#


from binascii import b2a_base64

from socket import gethostname, gethostbyname
from xmlrpclib import ServerProxy
from uuid import uuid4
from time import sleep, time
from scapy.all import Automaton, ATMT, TCP, bind_layers, conf, NoPayload

from PacketsTwistClasses import OpenFlow, CentralEngineObject




class PacketsTwist(Automaton):
    """
    Packets Twist Scapy Automaton
    """

    def parse_args(self, user, epConfig, OFPort=None, _uid=None, **kargs):
        Automaton.parse_args(self, **kargs)
        self.PAUSED = False
        self.OFPort = (OFPort, 6633)[OFPort is None]

        # openflow packet model connect
        bind_layers(TCP, OpenFlow, sport=self.OFPort)
        bind_layers(TCP, OpenFlow, dport=self.OFPort)

        # packet filters
        self.filters = kargs.pop('filters', None)

        # user
        self.username = user
        self.userip = gethostbyname(gethostname())
        self.userhost = gethostname()

        self.epConfig = epConfig
        _epConfig = list(set([(ep['CE_IP'], ep['CE_PORT'])
                                    for ep in self.epConfig if ep['ENABLED']]))
        self.ceObjects = [
            CentralEngineObject(
                ServerProxy('http://{ip}:{port}/'.format(ip=ep[0], port=ep[1])),
            )
            for ep in _epConfig
        ]

        self.ceTraffic = [(ep[0], ep[1]) for ep in _epConfig]

        self.uid = (uuid4(), _uid)[_uid is not None]

        self.reinitRetries = 0
        self.reinitMaxRetries = 4

    def master_filter(self, packet):
        # default filter: exclude CE traffic
        packetHead = self.packet_head(packet)
        if ((packet_head['source']['ip'], packet_head['source']['port'])
                                                            in self.ceTraffic or
            (packet_head['destination']['ip'], packet_head['destination']['port'])
                                                            in self.ceTraffic):
            return False

        if not self.filter: return True

        filterStatus = True
        if self.filters.has_key('-i'):
            try:
                conf.iface = self.filters['-i']
            except Exception, e:
                filterStatus = False

                print 'PT debug: parse arguments exception: {ex}'.format(ex=e)

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
                                            packetHead['source']['port'])

        if self.filters.has_key('-port_dst'):
            filterStatus = (self.filters['-port_dst'] ==
                                            packetHead['destination']['port'])

        if self.filters.has_key('-ip_src'):
            filterStatus = (self.filters['-ip_src'] ==
                                            packetHead['source']['ip'])

        if self.filters.has_key('-ip_dst'):
            filterStatus = (self.filters['-ip_dst'] ==
                                            packetHead['destination']['ip'])

        return filterStatus


    def packet_parse(packet):
        source = {}
        destination = {}
        try:
            source['mac'] = packet.fields['src']
            destination['mac'] = packet.fields['dst']

            try:
                source['ip'] = packet.payload.fields['src']
                destination['ip'] = packet.payload.fields['dst']
            except Exception, e:
                source['ip'] = 'None'
                destination['ip'] = 'None'

                print 'PT debug: packet head exception (ip): {ex}'.format(ex=e)

            try:
                source['port'] = packet.payload.payload.fields['sport']
                destination['port'] = packet.payload.payload.fields['dport']
            except Exception, e:
                source['port'] = 'None'
                destination['port'] = 'None'

                print 'PT debug: packet head exception (port): {ex}'.format(ex=e)
        except Exception, e:
            source['mac'] = 'None'
            destination['mac'] = 'None'

            print 'PT debug: packet head exception (mac): {ex}'.format(ex=e)

        data = {
            'protocol': packet.payload.payload.name,
            'source': source,
            'destination': destination,
        }

        return data

    def reinit(self):
        print 'PT debug: reinit ..'

        self.parse_args(self.username, self.epConfig, self.OFPort, self.uid)

        raise self.BEGIN()

    def ce_status_update(self):
        # Try to ping status from CE!
        for ce in self.ceObjects:
            try:
                response = ce.proxy.echo('ping')
                self.reinitRetries = 0
            except Exception, e:
                self.ceObjects.pop(self.ceObjects.index(ce))

                print 'PT warning: Central Engine is down .... [{0}]'.format(e)

                if len(self.ceObjects) == 0:
                    if self.reinitRetries < self.reinitMaxRetries:
                        print 'PT debug: no central engines; \
                                will retry [{r}] ..'.format(r=self.reinitRetries)
                        self.reinitRetries += 1

                        _epConfig = list(set([(ep['CE_IP'], ep['CE_PORT'])
                                    for ep in self.epConfig if ep['ENABLED']]))
                        self.ceObjects = [
                            CentralEngineObject(
                                ServerProxy('http://{ip}:{port}/'.format(ip=ep[0],
                                                                    port=ep[1])),
                            )
                            for ep in _epConfig
                        ]

                        sleep(2)

                        raise self.BEGIN()
                    else:
                        raise self.END()


    # BEGIN
    @ATMT.state(initial=1)
    def BEGIN(self):
        print '|||| state: BEGIN ||||'
        print 'started sniff ..'

        self.ce_status_update()

        args = {
            'command': 'registersniff',
            'data': str(self.uid)
        }

        try:
            for ce in self.ceObjects:
                # create user if ep is not running
                ce.proxy.getExecStatusAll(self.username)

                pluginData = ce.proxy.runPlugin(self.username, 'SNIFF', args)
                if pluginData['status']['success']:
                    print 'registered to central engine %s..' % ce.proxy
                else:
                    print 'running unregistered to central engine %s ..' % ce.proxy
                    print pluginData['status']['message']
        except Exception, e:
            print 'PT debug: [BEGIN] {err}'.format(err=e)

        raise self.WAITING()


    # WAITING
    @ATMT.state()
    def WAITING(self):
        self.ce_status_update()

        restart = False

        try:
            for ce in self.ceObjects:
                args = {
                    'command': 'None',
                    'data': str(self.uid)
                }
                args['command'] = 'echo'
                pluginData = ce.proxy.runPlugin(self.username, 'SNIFF', args)

                ce.pluginStatus = pluginData['state']
                self.filters = pluginData['data']['filters']

                if ce.pluginStatus == 'restart':
                    args['command'] = 'restarted'
                    ce.proxy.runPlugin(self.username, 'SNIFF', args)

                    print 'PT debug: sniffer restart ..\n'

                    restart = True

                else:
                    ce.PAUSED = not ce.pluginStatus == 'running'

                _paused = self.PAUSED

                self.PAUSED = (sum([ce.PAUSED for ce in self.ceObjects])
                                == len(self.ceObjects))

                if not _paused == self.PAUSED:
                    print 'PT debug: sniffer paused status chaged: \
                                                {s}'.format(s=self.PAUSED)
        except Exception, e:
            print 'PT debug: [WAITING] {err}'.format(err=e)

        if restart: self.reinit()


    # RECEIVING
    @ATMT.receive_condition(WAITING)
    def receive_data(self, pkt):
        raise (self.RECEIVING(pkt), self.WAITING())[self.PAUSED]


    # RECEIVED
    @ATMT.state()
    def RECEIVING(self, packet):
        data = {
            'sniffer': {
                'ip': self.userip,
                'hostname': self.userhost,
                'username': self.username,
            },
            'packet_head': self.packet_head(packet),
            'packet': str(packet),
        }
        data['packet_head'].update([('id', str(time())), ])
        data = b2a_base64(str(data))

        self.ce_status_update()

        # push packet to central engines
        try:
            for ce in self.ceObjects:
                ce.proxy.runPlugin(self.username,
                                    'SNIFF', {'command': 'pushpkt', 'data': data})
        except Exception, e:
            print 'PT debug: [RECEIVING] {err}'.format(err=e)

        raise self.WAITING()


    """
    # EVENTS
    @ATMT.ioevent(BEGIN, name='commands')
    def transition(self, fd):
        commands = ['stop', 'restart', 'pause', 'resume']

        command = fd.recv()

        if command in commands:
            print 'PT debug: got command {cmd}'.format(cmd=command)
            if command == 'stop':

                raise self.END()

            elif command == 'restart':

                self.restart()

            elif command in ['pause', 'resume']:
                self.PAUSED = (True, False)[self.PAUSED]

                raise self.WAITING()
    """


    # END
    @ATMT.state(final=1)
    def END(self):
        #pluginData = ce.proxy.runPlugin() ## TO DO set plugin stop ??
        print '|||| state: END ||||'
