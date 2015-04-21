# coding: utf-8

"""
Interface with systemctl
"""

from pyshc.sh import Sh

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
        if header.startswith('*') or header.startswith('\xe2\x97\x8f'):
            name = map(str.strip, header.split(' - '))
            vals['header'] = ' '.join(name[1:])

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
    def header(self):
        return self._vals['header']

    @property
    def loaded(self):
        return self._vals['Loaded']

    @property
    def active(self):
        return self._vals['Active']

    @property
    def pid(self):
        return self._vals['Main PID']

    @property
    def cgroup(self):
        return self._vals['CGroup']


class Status(object):
    """
    Interpretation of the `ParsedStatus` values.
    """

    def __init__(self, status):
        """Create a `Status` instance.

        :param status: the parsed status
        :type status: :class:`ParsedStatus`
        """
        self._status = status

    def is_loaded(self):
        "Is the service loaded?"
        return self._status.loaded.startswith('loaded')

    def is_active(self):
        return self._status.active.startswith('active')

    @property
    def pid(self):
        """Get the PID of the service.
        Throws an OSError if it is not running

        :returns: the process id
        :rtype: :class:`int`
        """
        try:
            pid_str = self._status.pid
        except ValueError:
            raise OSError('{} is not running'.format(self._status.name))

        pid = int(pid_str.split()[0])
        return pid

    @property
    def cgroup(self):
        """Get the CGroup path.
        Throws OSError if it is not running.

        :returns: the CGroup path
        :rtype: :class:`str`
        """
        "The CGroup path"
        try:
            return self._status.cgroup
        except ValueError:
            raise OSError('{} is not running'.format(self._status.name))


class Systemctl(object):

    def __init__(self):
        self.systemctl = systemctl_command

    def status(self, service):
        return self.systemctl(['status', service, '-n', '0'])
