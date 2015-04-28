# coding: utf-8

"""
Interface with systemctl
"""

from pyshc.sh import Sh
from base import AbstractServiceManager, AbstractStatus


systemctl_command = Sh('systemctl')


class ParsedStatus(object):
    """
    Representation of the raw output from running
    ``systemctl status <service>``
    """

    def __init__(self, vals=None):
        self._vals = vals or dict()

    @classmethod
    def from_systemctl_output(cls, string):
        vals = dict()
        for line in string.split('\n'):
            k,v = line.strip().split('=', 1)
            vals[k] = v
        return cls(vals=vals)

    @classmethod
    def from_systemctl_status_output(cls, string):
        """Parse the output from 'systemctl status <name>'

        :param cls: the class
        :param string: the output string
        :returns: the status
        :rtype: :class:`Status`
        """

        # extract these values from the output string
        match_on = set(['Loaded',
                        'Active',
                        'Main PID',
                        'CGroup'])
        vals = dict()  # destination

        # header
        lines = string.split('\n')
        header = lines[0]
        # star (*) or fancy dot (●)
        fancy_dot = '\xe2\x97\x8f'
        if header.startswith('*') or header.startswith(fancy_dot):
            vals['header'] = header
            header = header.lstrip('*').lstrip(fancy_dot).strip()
            name, description = map(str.strip, header.split(' - '))
            vals['name'] = name
            vals['description'] = description

        # remaining lines
        for line in lines:
            line = line.strip()
            split = line.split(':')

            # the case where line has no colon (:)
            if len(split) < 2:
                continue

            start, rest = split[0], ':'.join(split[1:]).strip()
            if start in match_on:
                vals[start] = rest

        return cls(vals=vals)

    @property
    def id(self):
        return self._vals['Id']

    @property
    def names(self):
        return self._vals['Names']

    @property
    def description(self):
        return self._vals['Description']

    @property
    def load_state(self):
        return self._vals['LoadState']

    @property
    def active_state(self):
        return self._vals['ActiveState']

    @property
    def main_pid(self):
        return self._vals['MainPID']

    @property
    def control_group(self):
        return self._vals['ControlGroup']


class Status(AbstractStatus):
    """
    Interpretation of the `ParsedStatus` values.
    """

    def __init__(self, status):
        """Create a `Status` instance.

        :param status: the parsed status
        :type status: :class:`ParsedStatus`
        """
        self._status = status

    @property
    def pid(self):
        """Get the PID of the service.
        Throws an OSError if it is not running

        :returns: the process id
        :rtype: :class:`int`
        """

        # The documentation for the MainPID systemd property has been
        # elusive. Experimentation shows that a value of 0 (zero)
        # indicates that the service is *not* running.

        pid_val = self._status.main_pid
        pid = int(pid_val.strip())
        if pid > 0:
            return pid
        else:
            raise OSError('{} is not running'.format(self._status.id))

    @property
    def name(self):
        return self._status.id

    @property
    def running(self):
        try:
            self.pid
            return True
        except OSError:
            return False


class Systemctl(AbstractServiceManager):

    def __init__(self, *args, **kwargs):
        AbstractServiceManager.__init__(self, *args, **kwargs)
        self._command = self.create_command('systemctl')

    @property
    def service(self):
        return self._command

    def start(self):
        self.service(['start', self.service_name])
        return self.status()

    def stop(self):
        self.service(['stop', self.service_name])
        return self.status()

    def status(self):
        raw = self.service(['show', self.service_name])
        parsed = ParsedStatus.from_systemctl_output(raw)
        status = Status(parsed)
        return status

