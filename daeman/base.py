import psutil
import os.path
import os


class Manager(object):
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

    def __init__(self, pidfile=None, logfile=None, keep_logs=False):
        self._pidfile = pidfile
        self._logfile = logfile

    def start(self):
        """Start a managed process
        """
        raise NotImplementedError

    def stop(self):
        """Stop a managed process
        """
        raise NotImplementedError

    def status(self):
        """Check if the managed process is running

        :returns: the running state
        :rtype: bool

        """
        if not os.path.exists(self._pidfile):
            return False

        with open(self._pidfile) as fd:
            pid_str = fd.read().strip()
        pid = int(pid_str)

        if not psutil.pid_exists(pid):
            self._cleanup()
            return False
        else:
            return True

    def health(self):
        raise NotImplementedError

    def _clean(self):
        """Cleanup once the managed process is no longer running.

        It is the responsibility of the calling function to ensure
        that the managed process is not running.
        """
        if os.path.exists(self._pidfile):
            os.unlink(self._pidfile)

        
