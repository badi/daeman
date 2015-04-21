

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

    def __init__(self, pidfile=None, logfile=None):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError
