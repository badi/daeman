
from pyshc.sh import Sh
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractStatus:
    """The status of a queried process"""

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        "The name of the service"

    @abstractproperty
    def running(self):
        "Is the service running?"

    @abstractproperty
    def pid(self):
        """The process id if running.
        Raises OSError if not running
        """

class AbstractServiceManager:
    """Provide the basic API for the following functionality dealing with
    external, long-running processes:

    - start
    - stop
    - health-check/monitoring
    - daemonizing

    Processes started thus should continue executing even if the
    parent process (this one) exits. Upon resumption, the manager
    should load the current state of the managed process.
    """

    __metaclass__ = ABCMeta

    def __init__(self, service_name, sudo=False):
        """
        :param service_name: the name of the service to manage

        """
        self._service_name = service_name
        self._sudo = sudo

    @property
    def service_name(self):
        return self._service_name

    @property
    def using_sudo(self):
        "Is 'sudo' used to manage the service?"
        return self._sudo

    @abstractproperty
    def service(self):
        "The command to control the service"

    def create_command(self, command):
        if self.using_sudo:
            cmd = Sh('sudo', args=command)
        else:
            cmd = Sh(command)
        return cmd

    @abstractmethod
    def start(self, ):
        """Start a managed process
        """

    @abstractmethod
    def stop(self):
        """Stop a managed process
        """

    @abstractmethod
    def status(self):
        """Check if the managed process is running

        :returns: the running state
        :rtype: bool

        """

    def health(self):
        """Get some information about the health of the process.

        Currently this just returns the status.

        :returns: status of the process
        """
        return self.status()

