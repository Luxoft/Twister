
# version: 2.002

from __future__ import print_function
from __future__ import with_statement

import time
import rpyc
import threading
from threading import Thread
from thread import allocate_lock

import unittest


# # # # #
# Testing X number of sim connections.
# # # # #


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self.daemon = False
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            try:
                self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            except:
                trace = traceback.format_exc()[34:].strip()
                print('Exception::', trace)


class Test1(unittest.TestCase):

    cePath = ('localhost', 8008)
    userName = 'user'
    max_clients = 300
    conn_lock = allocate_lock()


    def makeConnection(self, identifier):
        proxy = False
        with self.conn_lock:
            # Connect to RPyc server
            try:
                ce_ip, ce_port = self.cePath
                proxy = rpyc.connect(ce_ip, ce_port)
            except:
                print('*ERROR* Cannot connect to CE path `{}`! Exiting!'.format(self.cePath))
                return False
            # Authenticate on RPyc server
            try:
                check = proxy.root.login(self.userName, 'EP')
                proxy.root.hello(identifier)
                # print('Connect and authenticate to CE at `{}` is OK.'.format(self.cePath))
            except:
                check = False
            if not check:
                print('*ERROR* Cannot authenticate on CE path `{}`! Exiting!'.format(self.cePath))
                return False
        # Success
        return proxy


    def test_a_serial(self):
        """
        Testing max nr of virtual clients.
        """
        print('Testing `{}` clients in serial...'.format(self.max_clients))
        conns = []
        for i in range(100, self.max_clients+100):
            c = self.makeConnection('client::' + str(i))
            if not c: continue
            print( c.root.echo('Hi there! Serial client `{}` here!'.format(c._config['connid'])) )
            c.root.listEPs()
            c.root.listLibraries()
            c.close() ; del c
            conns.append(True)
        print('Made `{}` serial client connections.'.format(len(conns)))
        self.assertEqual(len(conns), self.max_clients)


    def test_b_parallel(self):
        """
        Testing max nr of virtual clients.
        """
        def hello(i=1):
            c = self.makeConnection('client::' + str(i))
            time.sleep(0.5)
            if not c: return False
            print( c.root.echo('Hi there! Parallel client `{}` here!'.format(c._config['connid'])) )
            c.root.listEPs()
            c.root.listLibraries()
            c.close() ; del c
            return True

        conns = []
        print('Testing `{}` clients in parallel...'.format(self.max_clients))

        for i in range(100, self.max_clients+100):
            t = ThreadWithReturnValue(target=hello, kwargs={'i':i})
            conns.append(t)

        [t.start() for t in conns]
        [t.join() for t in conns]
        result = [t._return for t in conns if t._return]
        del conns
        print('Made `{}` parallel client connections. Threads remaninig: `{}`.'.format(len(result), threading.activeCount()))

        self.assertEqual(len(result), self.max_clients)


# # #


if __name__ == '__main__':
    unittest.main()


# Eof()
