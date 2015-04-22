"""
Interaction with Upstart ``initctl`` command
"""

from pyshc.sh import Sh

initctl_command = Sh('initctl')


class ManagerAPI(object):

    def status(self):
        raise NotImplementedError


class StatusResult(object):
    "The raw output of running ``initctl status <service>``"

    def __init__(self, vals=None):
        """
        :param vals: the parsed output of ``initctl status``
        """
        self._vals = vals or dict()

    @classmethod
    def from_initctl_output(cls, string):
        """Parse the output from ``systemctl status <name>``

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
            pid_str = words[-1]
            vals['process'] = int(pid_str)

        return cls(vals=vals)

    @property
    def name(self):
        "The name of the service"
        return self._vals['name']

    @property
    def goal(self):
        "The target goal of the process"
        return self._vals['goal']

    @property
    def state(self):
        "The state of the services towards the goal"
        return self._vals['state']

    @property
    def running(self):
        "Is the service running?"
        return 'process' in self._vals

    @property
    def process(self):
        "The process ID of the service"
        return self._vals['process']