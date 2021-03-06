"""
Interaction with Upstart ``initctl`` command
"""

from base import AbstractServiceManager, AbstractStatus
from pyshc.sh import CalledProcessError


class Status(AbstractStatus):
    "The raw output of running ``initctl status <service>``"

    def __init__(self, vals=None):
        """
        :param vals: the parsed output of ``initctl status``
        """
        self._vals = vals or dict()

    @classmethod
    def from_initctl_output(cls, string):
        """Parse the output from ``systemctl status <name>``

        See man 8 init for job goals and state transitions

        :param string: the output string
        :returns: the status result
        :rtype: instance of :class:`StatusResult`
        """
        vals = dict()

        # split on whitespace
        words = string.strip().split()

        # first element is the name of the service
        name, words = words[0], words[1:]
        vals['name'] = name

        # the target goal and status towards goal
        state, words = words[0], words[1:]
        goal, state = state.rstrip(',').split('/')
        vals['goal'] = goal
        vals['state'] = state

        # get PID if running
        if goal == 'start' and state == 'running':
            pid = words[-1]
            vals['process'] = pid

        return cls(vals=vals)

    @property
    def name(self):
        "The name of the service"
        return self._vals['name']

    @property
    def running(self):
        "Is the service running?"
        return 'process' in self._vals

    @property
    def pid(self):
        "The process ID of the service"
        pidstr = self._vals['process']
        return int(pidstr)


class Initctl(AbstractServiceManager):
    """Manage a service

    ::

      ssh = Initctl('ssh')
      ssh.status().running
      # False
      status = ssh.start()
      status.goal
      # start
      status.state
      # pre-start
      status.running
      # False
      ssh.status().running
      # True
    """

    def __init__(self, *args, **kwargs):
        AbstractServiceManager.__init__(self, *args, **kwargs)
        self._command = self.create_command('initctl')

    @property
    def service(self):
        return self._command

    def start(self):
        try:
            self.service('start {}'.format(self.service_name))
        except CalledProcessError:
            pass
        return self.status()

    def stop(self):
        try:
            self.service('stop {}'.format(self.service_name))
        except CalledProcessError:
            pass
        return self.status()

    def status(self):
        output = self.service('status {}'.format(self.service_name))
        status = Status.from_initctl_output(output)
        return status
