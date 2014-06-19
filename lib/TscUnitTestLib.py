
# File: TscUnitTestLib.py ; This file is part of Twister.

# version: 3.001

# Copyright (C) 2012-2014, Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

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
This module contains Setup, Teardown controls.
All functions that begin with "test" will be executed automatically,
in alphabetic order.
Twister Test implements the same methods as Python Unit Test.
'''

#

def safe_repr(obj, short=False):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    return result

#

class TwisterTest(object):

    def __init__(self):
        # All tests that will be executed automatically,
        # must begin with the test idenfier.
        self.test_identifier = 'test'


    def __find_tests(self):
        tests = [x for x in sorted(dir(self)) if x.startswith(self.test_identifier) and x != 'test_identifier']
        return tests

    def __str__(self):
        tests = self.__find_tests()
        return "<%s tests=%s>" % (self.__class__, tests)

    def __iter__(self):
        tests = self.__find_tests()
        for t in tests:
            yield t


    def setUpClass(self):
        pass

    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        if not expr:
            msg = msg or '{} is not true'.format(safe_repr(expr))
            raise AssertionError(msg)

    def assertFalse(self, expr, msg=None):
        """Check that the expression is false."""
        if expr:
            msg = msg or '{} is not false'.format(safe_repr(expr))
            raise AssertionError(msg)

    def assertEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '==' operator."""
        if not first == second:
            msg = msg or '{} != {}'.format(safe_repr(first), safe_repr(second))
            raise AssertionError(msg)

    def assertNotEqual(self, first, second, msg=None):
        """Fail if the two objects are equal as determined by the '==' operator."""
        if not first != second:
            msg = msg or '{} == {}'.format(safe_repr(first), safe_repr(second))
            raise AssertionError(msg)

    def assertIn(self, member, container, msg=None):
        """Just like self.assertTrue(a in b), but with a nicer default message."""
        if member not in container:
            msg = msg or '{} not found in {}'.format(safe_repr(member), safe_repr(container))
            raise AssertionError(msg)

    def assertNotIn(self, member, container, msg=None):
        """Just like self.assertTrue(a not in b), but with a nicer default message."""
        if member in container:
            msg = msg or '{} unexpectedly found in {}'.format(safe_repr(member), safe_repr(container))
            raise AssertionError(msg)

    def assertIs(self, expr1, expr2, msg=None):
        """Just like self.assertTrue(a is b), but with a nicer default message."""
        if expr1 is not expr2:
            msg = msg or '{} is not {}'.format(safe_repr(expr1), safe_repr(expr2))
            raise AssertionError(msg)

    def assertIsNot(self, expr1, expr2, msg=None):
        """Just like self.assertTrue(a is not b), but with a nicer default message."""
        if expr1 is expr2:
            msg = msg or 'unexpectedly identical: {}'.format(safe_repr(expr1))
            raise AssertionError(msg)

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise AssertionError(msg)


    def run(self):
        try:
            self.setUpClass()
        except Exception, e:
            print('SetUpClass function crashed with exception: `{}` !'.format(e))
            return -1

        failed = False
        tests = self.__find_tests()

        for test in tests:
            try:
                self.setUp()
            except Exception, e:
                print('SetUp function crashed with exception: `{}` !'.format(e))

            func = getattr(self, test)
            try:
                func()
            except AssertionError, e:
                print('Test `{}` assertion error: `{}`.'.format(test, e))
                failed = True
            except Exception, e:
                print('Test `{}` crashed with exception: `{}`.'.format(test, e))
                failed = True

            try:
                self.tearDown()
            except Exception, e:
                print('TearDown function crashed with exception: `{}` !'.format(e))

        try:
            self.tearDownClass()
        except Exception, e:
            print('TearDownClass function crashed with exception: `{}` !'.format(e))
            return -1

        if not failed:
            return 'PASS'
        else:
            return 'FAIL'


    def main(self):
        return self.run()

#

TestCase = TwisterTest

#
