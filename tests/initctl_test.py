from daeman.initctl import ManagerAPI
from unittest import TestCase
from inspect import getargspec
from nose.plugins.attrib import attr


@attr(service='upstart')
class CheckManagerAPI(object):
    """Ensure that `clazz` provides methods matching the expected API

    The fields below needs to be defined in the ``setUp`` method of
    the inheriting class.
    """

    argnames = None  # :: list of str
    keywords = None  # :: list of (str, val)
    defaults = None  # :: list of val

    def test_num_args(self):
        "Test the number of function parameters"
        self.assertEqual(len(self.argnames), len(self.keywords))

    def test_arg_names_and_default(self):
        "Make sure that the parameter names and default values match"
        for i, (name, default) in enumerate(self.keywords):
            self.assertEqual(name, self.argnames[i])
            self.assertEqual(self.defaults[i], default)


@attr(service='upstart')
class TestManagerAPI_status(CheckManagerAPI, TestCase):

    def setUp(self):
        self.keywords = list()
        args, _, _, defaults = getargspec(ManagerAPI.status)
        self.argnames = args[1:]
        self.assertIsNone(defaults)
        self.defaults = list()
