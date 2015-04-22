from daeman.systemctl import systemctl_command, ParsedStatus, Status, Systemctl
from unittest import TestCase
from nose.plugins.attrib import attr


@attr(service='systemd')
class SetupParseStatusTests:
    def setUp(self):
        self.status_string = systemctl_command('status sshd.service -n 0')


@attr(service='systemd')
class TestParsedStatusParser(SetupParseStatusTests, TestCase):

    def test_from_systemctl_output(self):
        "Ensure that the parser works"
        ParsedStatus.from_systemctl_output(self.status_string)


@attr(service='systemd')
class TestParsedStatus(SetupParseStatusTests, TestCase):

    def setUp(self):
        SetupParseStatusTests.setUp(self)
        self.status = ParsedStatus.from_systemctl_output(self.status_string)

    def test_header(self):
        "Ensure the header is parsed"
        self.assertTrue(len(self.status.header) > 0)

    def test_loaded(self):
        "Ensure that the 'Loaded' field is parsed"
        self.assertTrue(len(self.status.loaded) > 0)

    def test_active(self):
        "Ensure that the 'Active' field is parsed"
        self.assertTrue(len(self.status.active) > 0)

    def test_pid(self):
        "Ensure that the 'Main PID' field is parsed"
        self.assertTrue(len(self.status.pid) > 0)

    def test_cgroup(self):
        "Ensure that the 'CGroup' field is parsed"
        self.assertTrue(len(self.status.cgroup) > 0)


@attr(service='systemd')
class TestStatus(TestCase):
    def setUp(self):
        output = systemctl_command('status sshd.service -n 0')
        parsed = ParsedStatus.from_systemctl_output(output)
        self.status = Status(parsed)

    def test_is_loaded(self):
        "The service should be loaded"
        self.assertTrue(self.status.is_loaded())

    def test_is_active(self):
        "The service should active"
        self.assertTrue(self.status.is_active())

    def test_pid(self):
        "The service should have a PID"
        pid = self.status.pid
        self.assertIsInstance(pid, int)

    def test_cgroup(self):
        "The service should have a cgroup path"
        path = self.status.cgroup
        self.assertIsInstance(path, str)
        self.assertTrue(path.startswith('/'))


@attr(service='systemd')
class TestSystemctl(TestCase):
    def setUp(self):
        self.systemctl = Systemctl()

    def test_status(self):
        "The 'status' method should work"
        self.systemctl.status('sshd.service')
