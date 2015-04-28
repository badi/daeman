from daeman.systemctl import systemctl_command, ParsedStatus, Status, Systemctl
from unittest import TestCase
from nose.plugins.attrib import attr
from api_check_util import CheckStatusAPI, CheckServiceRunning, CheckServiceStopped


@attr(service='systemd')
class TestParsedStatusParser(TestCase):

    def setUp(self):
        self.status_string = systemctl_command('show sshd.service')

    def test_from_systemctl_output(self):
        "Ensure that the parser works"
        ParsedStatus.from_systemctl_output(self.status_string)


@attr(service='systemd')
class TestStatus(CheckStatusAPI, TestCase):
    name = 'sshd.service'
    running = True

    def get_status(self):
        raw = systemctl_command('show {}'.format(self.name))
        parsed = ParsedStatus.from_systemctl_output(raw)
        status = Status(parsed)
        return status


@attr(service='systemd')
class TestSystemctlStarted(CheckServiceRunning, TestCase):
    manager = Systemctl
    service_name = 'sshd.service'
    status_class = Status


@attr(service='systemd')
class TestSystemctlStopped(CheckServiceStopped, TestCase):
    manager = Systemctl
    service_name = 'sshd.service'
    status_class = Status
