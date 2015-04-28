"""This test module checks that the API provided in the base.Manager
class is as expected.
"""

from util import inspect_function_args
from unittest import TestCase
from daeman.base import AbstractServiceManager


class CheckAPI(object):
    """Ensure that the API is as expected.
    """

    # expected
    args_exp = list()      # :: [str]
    keywords_exp = dict()  # :: {str -> val}

    # actual
    args = None      # :: [str]
    keywords = None  # :: {str -> val}

    def test_num_args(self):
        "Test the number of function parameters"
        expected = len(self.args_exp) + len(self.keywords_exp)
        actual = len(self.args) + len(self.keywords)
        self.assertEqual(expected, actual,
                         'expected {} but got {}'.format(
                             [self.args_exp, self.keywords_exp],
                             [self.args, self.keywords]))

    def test_args(self):
        "test the name of the arguments"
        for expected, actual in zip(self.args_exp, self.args):
            self.assertEqual(expected, actual)

    def test_keywords(self):
        "Make sure that the parameter names and default values match"
        for name, default in self.keywords_exp.items():
            self.assertIn(name, self.keywords)
            self.assertEqual(default, self.keywords[name])


class TestManagerInit(TestCase, CheckAPI):
    "The constructor"

    args_exp = ['service_name']
    keywords_exp = dict(sudo=False)

    def setUp(self):
        self.args, self.keywords = \
            inspect_function_args(AbstractServiceManager.__init__)


class TestManagerStart(TestCase, CheckAPI):
    "The 'start' method"

    def setUp(self):
        self.args, self.keywords = \
            inspect_function_args(AbstractServiceManager.start)


class TestManagerStop(TestCase, CheckAPI):
    "The 'stop' method"

    def setUp(self):
        self.args, self.keywords = \
            inspect_function_args(AbstractServiceManager.stop)


class TestManagerStatus(TestCase, CheckAPI):
    "The 'status' method"

    def setUp(self):
        self.args, self.keywords = \
            inspect_function_args(AbstractServiceManager.status)


class TestManagerHealth(TestCase, CheckAPI):
    "The 'health' method"

    def setUp(self):
        self.args, self.keywords = \
        inspect_function_args(AbstractServiceManager.health)


