
# File: UnitTest.py ; This file is part of Twister.

# version: 2.001

# Copyright (C) 2012-2013 , Luxoft

# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This module contains Setup, Teardown controls and Step.
Twister Test implements the same methods as Python Unit Test.
'''

#

class TwisterTest:

    def __init__(self):
        # All tests that will be executed automatically,
        # must begin with the test idenfier.
        self.test_identifier = 'test'


    def __find_tests(self):
        tests = [x for x in dir(self) if x.startswith(self.test_identifier) and x != 'test_identifier']
        return tests

    def __str__(self):
        tests = self.__find_tests()
        return "<%s tests=%s>" % (self.__class__, tests)

    def __iter__(self):
        tests = self.__find_tests()
        for t in tests:
            yield t


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def run(self):
        try:
            self.setUp()
        except Exception, e:
            print('SetUp function crashed with exception: `{}`.'.format(e))
            return -1

        vals = []
        tests = self.__find_tests()

        for test in tests:
            func = getattr(self, test)
            try:
                v = func()
            except Exception, e:
                print('Test name `{}` crashed with exception: `{}`.'.format(test, e))
                v = -1
            vals.append(v)

        try:
            self.tearDown()
        except Exception, e:
            print('TearDown function crashed with exception: `{}`.'.format(e))
            return -1

        # If FALSE is not in the list of results from all the tests,
        # It means that the UnitTest has passed !
        result = False not in [bool(x) for x in vals]

        if result:
            return 'PASS'
        else:
            return 'FAIL'


    def main(self):
        return self.run()

#

"""
from ce_libs import TwisterTest

# How to define a test:

class Test1(TwisterTest):

    def setUp(self):
        # connect to switch...
        print 'Preparing setup...'

    def tearDown(self):
        # connect to switch...
        print 'Running teardown...'

    def test1(self):
        # Testing some feature...
        print 'Testing feature 1...'
        return True

    def test2(self):
        # Testing some feature...
        print 'Testing feature 2...'
        return True

    def test3(self):
        # Testing some feature...
        print 'Testing feature 3...'
        # Don't return anything, this means FAIL

t1 = Test1()
print t1, '\n'
_RESULT = t1.main()
"""
