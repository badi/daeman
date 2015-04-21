"""This test module checks that the API provided in the base.Manager
class is as expected.
"""

from unittest import TestCase
from daeman.base import Manager
from inspect import getargspec


class CheckAPI(object):
    """Ensure that the API is as expected.


    Intended usage:
    ==============================

    - Subclass `TestCase` with a `CheckAPI` mixin.
    - provide a `setUp` method initializing:
      - self.keywords :: [(name (str), default value)]
      - self.argnames :: [name (str)]
      - defaults :: [(value)]


    Implementation details
    ==============================

    This uses the `getargspec` function from the builtin `inspect`
    module to examine the function arguments and default values.
pp
    The purpose of these tests is to check that the provided interface
    adheres to the expected API.

    """

    def test_num_args(self):
        "Test the number of function parameters"
        self.assertEqual(len(self.argnames), len(self.keywords))

    def test_arg_names_and_default(self):
        "Make sure that the parameter names and default values match"
        for i, (name, default) in enumerate(self.keywords):
            self.assertEqual(name, self.argnames[i])
            self.assertEqual(self.defaults[i], default)


class TestManagerInit(TestCase, CheckAPI):
    "The constructor"
    def setUp(self):
        self.keywords = [('pidfile', None),
                         ('logfile', None)]
        args, _, _, defaults = getargspec(Manager.__init__)
        self.argnames = args[1:]
        self.defaults = list(defaults)


class TestManagerStart(TestCase, CheckAPI):
    "The 'start' method"
    def setUp(self):
        self.keywords = []
        args, _, _, defaults = getargspec(Manager.start)
        self.argnames = args[1:]
        self.assertIsNone(defaults)
        self.defaults = list()


class TestManagerStop(TestCase, CheckAPI):
    "The 'stop' method"
    def setUp(self):
        self.keywords = []
        args, _, _, defaults = getargspec(Manager.stop)
        self.argnames = args[1:]
        self.assertIsNone(defaults)
        self.defaults = list()


class TestManagerStatus(TestCase, CheckAPI):
    "The 'status' method"
    def setUp(self):
        self.keywords = []
        args, _, _, defaults = getargspec(Manager.status)
        self.argnames = args[1:]
        self.assertIsNone(defaults)
        self.defaults = list()


class TestManagerHealth(TestCase, CheckAPI):
    "The 'health' method"
    def setUp(self):
        self.keywords = []
        args, _, _, defaults = getargspec(Manager.health)
        self.argnames = args[1:]
        self.assertIsNone(defaults)
        self.defaults = list()
