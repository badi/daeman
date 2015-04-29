
Introduction
======================================================================


Requirements
======================================================================

* System requirements: see ``requirements-system.csv``
* Python requirements: see ``requirements.txt``
* Development Python requirements: see ``requirements-devel.txt``


Usage
======================================================================

Daeman supports interactions with both the Upstart and Systemd init
processes. You can the init system to:

* start
* stop
* query the status

of various system services, such as the SSH daemon, or others.

For example, mange the SSH service on systemd:

.. code:: python
          from daeman.initctl import Initctl
          ssh = Initctl('ssh', sudo=True)
          if not ssh.status().running:
              ssh.start()
          status = ssh.status()
          print status.name
          print status.pid
