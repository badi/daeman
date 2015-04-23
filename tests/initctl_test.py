from util import inspect_function_args
from base_test import CheckAPI

from daeman.initctl import initctl_command, Status
from daeman.initctl import Manager
from unittest import TestCase
from nose.plugins.attrib import attr


class CheckManagerAPI_method(CheckAPI):

    method = None

    def setUp(self):
        method = getattr(Manager, self.method)
        self.args, self.keywords = inspect_function_args(method)


@attr(service='upstart')
class TestManagerAPI_status(CheckManagerAPI_method, TestCase):
    method = 'status'


@attr(service='upstart')
class TestManagerAPI_start(CheckManagerAPI_method, TestCase):
    method = 'start'


@attr(service='upstart')
class TestManagerAPI_stop(CheckManagerAPI_method, TestCase):
    method = 'stop'


@attr(service='upstart')
class TestStatusResult(TestCase):

    def setUp(self):
        self.output_ssh = initctl_command('status ssh')
        self.output_procps = initctl_command('status procps')

    def test_running_service(self):
        "Ensure that a running service is parsed"
        Status.from_initctl_output(self.output_ssh)

    def test_stopped_service(self):
        "Ensure that a stopped service is parsed"
        Status.from_initctl_output(self.output_procps)

    def test_running_service_correct(self):
        "Ensure that a running service is parsed correctly"
        status = Status.from_initctl_output(self.output_ssh)
        self.assertEqual(status.name, 'ssh')
        self.assertEqual(status.goal, 'start')
        self.assertEqual(status.state, 'running')
        self.assertIsInstance(status.process, int)
        self.assertGreater(status.process, 0)

    def test_stopped_service_correct(self):
        "Ensure that a stopped service is parsed correctly"
        status = Status.from_initctl_output(self.output_procps)
        self.assertEqual(status.name, 'procps')
        self.assertEqual(status.goal, 'stop')
        self.assertEqual(status.state, 'waiting')
        self.assertNotIn('process', status._vals)


@attr(service='upstart')
class TestManagerRunning(TestCase):

    def setUp(self):
        self.service = Manager('ssh')

    def test_status(self):
        "Check the 'status' method"
        status = self.service.status()
        self.assertIsInstance(status, Status)
        self.assertTrue(status.running)


@attr(service='upstart')
class TestManagerStopped(TestCase):

    def setUp(self):
        self.service = Manager('procps')

    def test_status(self):
        "Check the 'status' method"
        status = self.service.status()
        self.assertIsInstance(status, Status)
        self.assertFalse(status.running)
