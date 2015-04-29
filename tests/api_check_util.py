from daeman.base import AbstractServiceManager, AbstractStatus
from abc import ABCMeta, abstractmethod


class CheckStatusAPI:
    "API check for status implementations"

    __metaclass__ = ABCMeta

    name = ""
    running = False

    @abstractmethod
    def get_status(self):
        "Return the status object to validate"

    def preSetUpHook(self):
        "Run before executing :func:`setUp`"
        pass

    def preTearDownHook(self):
        "Run before executing :func:`tearDown`"
        pass

    def setUp(self):
        self.preSetUpHook()
        self.status = self.get_status()

    def tearDown(self):
        self.preTearDownHook()

    def test_name(self):
        self.assertEqual(self.status.name, self.name)

    def test_running(self):
        self.assertEqual(self.status.running, self.running)

    def test_pid(self):
        pid = self.status.pid
        self.assertIsInstance(pid, int)


class CheckServiceRunning:
    "Test a running service"
    manager = AbstractServiceManager
    service_name = ""  # name of the service (eg ssh)
    sudo = True
    status_class = AbstractStatus

    def setUp(self):
        self.service = self.manager(self.service_name, sudo=self.sudo)
        self.service.start()

    def tearDown(self):
        self.service.start()

    def test_status(self):
        "Get the status of a running service"
        status = self.service.status()
        self.assertIsInstance(status, self.status_class)
        self.assertTrue(status.running)

    def test_start(self):
        "Try to start a running service"
        self.service.start()
        status = self.service.status()
        self.assertIsInstance(status, self.status_class)
        self.assertTrue(status.running)

        return status

    def test_stop(self):
        "Try to stop a running service"

        status = self.service.status()
        self.assertTrue(status.running)
        status = self.service.stop()
        self.assertIsInstance(status, self.status_class)
        self.assertFalse(status.running)


class CheckServiceStopped:
    "Test a stopped service"
    manager = AbstractServiceManager
    service_name = ""
    sudo = True
    status_class = AbstractStatus

    def setUp(self):
        self.service = self.manager(self.service_name, sudo=self.sudo)
        self.service.stop()

    def tearDown(self):
        self.service.stop()

    def test_status(self):
        "Get the status of a stopped service"
        status = self.service.status()
        self.assertIsInstance(status, self.status_class)
        self.assertFalse(status.running)

    def test_start(self):
        "Try to start a stopped service"
        status = self.service.status()
        self.assertFalse(status.running)
        status = self.service.start()
        self.assertTrue(status.running)

    def test_stop(self):
        "Try to stop a stopped service"
        status = self.service.status()
        self.assertFalse(status.running)
        status = self.service.stop()
        self.assertFalse(status.running)
