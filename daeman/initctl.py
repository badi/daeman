"""
Interaction with Upstart ``initctl`` command
"""


class ManagerAPI(object):

    def status(self):
        raise NotImplementedError
