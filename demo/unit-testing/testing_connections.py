
# version: 2.001

from __future__ import print_function
from __future__ import with_statement

import rpyc
import unittest


# # #
# Testing X number of sim connections.
# # #


class Test1(unittest.TestCase):

    cePath = ('localhost', 8008)
    userName = 'user'
    max_clients = 20
    max_eps = 500


    def makeConnection(self, identifier):
        proxy = False
        # Connect to RPyc server
        try:
            ce_ip, ce_port = self.cePath
            proxy = rpyc.connect(ce_ip, ce_port)
            proxy.root.hello(identifier)
            print('EP Debug: Connected to CE at `{}`...'.format(self.cePath))
        except:
            print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(self.cePath))
            return False
        # Authenticate on RPyc server
        try:
            check = proxy.root.login(self.userName, 'EP')
            print('EP Debug: Authentication successful!\n')
        except:
            check = False
        if not check:
            print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(self.cePath))
            return False
        # Success
        return proxy


    def test1(self):
        """
        Testing max nr of clients.
        """
        print('Testing clients...')
        conns = []
        for i in range(100, self.max_clients+100):
            c = self.makeConnection('client::' + str(i))
            if not c: continue
            conns.append(c)
        print('Made `{}` client connections.'.format(len(conns)))
        for c in conns:
            c.root.echo('Hi there! Client `{}` here!'.format(c._config['connid']))
        self.assertEqual(len(conns), self.max_clients)


    def test2(self):
        """
        Testing max nr of EPs.
        """
        print('Testing EPs...')
        conns = []
        for i in range(100, self.max_eps+100):
            c = self.makeConnection('EP::Nr' + str(i))
            if not c: continue
            conns.append(c)
        print('Made `{}` EP connections.'.format(len(conns)))
        for c in conns:
            c.root.echo('Hi there! EP `{}` here!'.format(c._config['connid']))
        self.assertEqual(len(conns), self.max_eps)


# # #


if __name__ == '__main__':
    unittest.main()


# Eof()
