from daeman.initctl import Status, Initctl
from pyshc.sh import Sh, CalledProcessError
from unittest import TestCase
from nose.plugins.attrib import attr
from api_check_util import CheckStatusAPI, CheckServiceRunning, CheckServiceStopped

initctl_command = Sh('sudo', args='initctl')

@attr(service='upstart')
class TestStatus(CheckStatusAPI, TestCase):
    name = 'ssh'
    running = True

    def get_status(self):
        raw = initctl_command('status {}'.format(self.name))
        return Status.from_initctl_output(raw)

    def preSetUpHook(self):
        try:
            initctl_command('start {}'.format(self.name))
        except CalledProcessError, e:
            pass


@attr(service='upstart')
class TestInitctlRunning(CheckServiceRunning, TestCase):
    manager = Initctl
    service_name = 'ssh'
    status_class = Status


@attr(service='upstart')
class TestInitctlStopped(CheckServiceStopped, TestCase):
    manager =Initctl
    service_name = 'ssh'
    status_class = Status

# from util import inspect_function_args
# from base_test import CheckAPI

# from daeman.initctl import initctl_command, Status
# from daeman.initctl import Manager
# from unittest import TestCase
# from nose.plugins.attrib import attr
# from subprocess import CalledProcessError


# class CheckManagerAPI_method(CheckAPI):

#     method = None

#     def setUp(self):
#         method = getattr(Manager, self.method)
#         self.args, self.keywords = inspect_function_args(method)


# @attr(service='upstart')
# class TestManagerAPI_status(CheckManagerAPI_method, TestCase):
#     method = 'status'


# @attr(service='upstart')
# class TestManagerAPI_start(CheckManagerAPI_method, TestCase):
#     method = 'start'


# @attr(service='upstart')
# class TestManagerAPI_stop(CheckManagerAPI_method, TestCase):
#     method = 'stop'


# @attr(service='upstart')
# class TestStatusResult(TestCase):

#     def setUp(self):
#         self.output_ssh = initctl_command('status ssh')
#         self.output_procps = initctl_command('status procps')

#     def test_running_service(self):
#         "Ensure that a running service is parsed"
#         Status.from_initctl_output(self.output_ssh)

#     def test_stopped_service(self):
#         "Ensure that a stopped service is parsed"
#         Status.from_initctl_output(self.output_procps)

#     def test_running_service_correct(self):
#         "Ensure that a running service is parsed correctly"
#         status = Status.from_initctl_output(self.output_ssh)
#         self.assertEqual(status.name, 'ssh')
#         self.assertEqual(status.goal, 'start')
#         self.assertEqual(status.state, 'running')
#         self.assertIsInstance(status.process, int)
#         self.assertGreater(status.process, 0)

#     def test_stopped_service_correct(self):
#         "Ensure that a stopped service is parsed correctly"
#         status = Status.from_initctl_output(self.output_procps)
#         self.assertEqual(status.name, 'procps')
#         self.assertEqual(status.goal, 'stop')
#         self.assertEqual(status.state, 'waiting')
#         self.assertNotIn('process', status._vals)


# @attr(service='upstart')
# class TestManagerRunning(TestCase):

#     def setUp(self):
#         self.service = Manager('ssh', sudo=True)
#         self.was_running = self.service.status().running
#         if not self.was_running:
#             self.service.start()

#     def tearDown(self):
#         if not self.was_running and self.service.status().ruuning:
#             self.service.stop()

#     def test_status(self):
#         "Get the status of a running service"
#         status = self.service.status()
#         self.assertIsInstance(status, Status)
#         self.assertTrue(status.running)

#     def test_start(self):
#         "Try to start a running service"
#         with self.assertRaises(CalledProcessError) as catcher:
#             self.service.start()
#         self.assertIn('Job is already running', catcher.exception.output)

#         status = self.service.status()
#         self.assertIsInstance(status, Status)
#         self.assertTrue(status.running)

#     def test_stop(self):
#         "Try to stop a running service"
#         status = self.service.status()
#         self.assertTrue(status.running)
#         status = self.service.stop()
#         self.assertFalse(status.running)


# @attr(service='upstart')
# class TestManagerStopped(TestCase):

#     def setUp(self):
#         self.service = Manager('ssh', sudo=True)
#         self.was_running = self.service.status().running
#         if self.was_running:
#             self.service.stop()

#     def tearDown(self):
#         if self.was_running and not self.service.status().running:
#             self.service.start()

#     def test_status(self):
#         "Get the status of a stopped service"
#         status = self.service.status()
#         self.assertIsInstance(status, Status)
#         self.assertFalse(status.running)

#     def test_start(self):
#         "Try to start a stopped service"
#         status = self.service.status()
#         self.assertFalse(status.running)
#         status = self.service.start()
#         self.assertTrue(status.running)

#     def test_stop(self):
#         "Try to stop a stopped service"
#         status = self.service.status()
#         self.assertFalse(status.running)
#         with self.assertRaises(CalledProcessError) as catcher:
#             self.service.stop()
#         self.assertIn('Unknown instance', catcher.exception.output)
