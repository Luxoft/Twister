
# version: 2.001

from ce_libs import TwisterTest

#
# <title>Unit Test Library</title>
# <description>This test is checking the Unit Test.</description>
#

class Test1(TwisterTest):

    def setUpClass(self):
        # connect to switch...
        print 'Preparing general setup...'

    def tearDownClass(self):
        # connect to switch...
        print 'Running general teardown...'

    def setUp(self):
        # connect to switch...
        print 'Preparing setup...'

    def tearDown(self):
        # connect to switch...
        print 'Running teardown...'


    def test1(self):
        # Testing some feature...
        print 'Testing assertTrue...'
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertTrue(0)

    def test2(self):
        # Testing some feature...
        print 'Testing assertEqual...'
        self.assertEqual('a', 'a')
        self.assertNotEqual('a', 'b')
        self.assertEqual('a', 'b')

    def test3(self):
        # Testing some feature...
        print 'Testing assertIn...'
        self.assertIn('x', ['x','y','z'])
        self.assertNotIn('a', ['x','y','z'])
        self.assertIn('x', ['y','z'])

    def test4(self):
        # Testing some feature...
        print 'Testing assertIs...'
        a = 1
        b = a
        c = 2
        self.assertIs(a, b)
        self.assertIsNot(a, c)
        self.assertIsNot(a, b)

    def test5(self):
        # Testing some feature...
        print 'Testing crash...'
        print self.xyz

t1 = Test1()
print t1, '\n'
_RESULT = t1.main()
