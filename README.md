[![Build Status](https://travis-ci.org/badi/daeman.svg?branch=master)](https://travis-ci.org/badi/daeman)

# Introduction

Daeman, short for DAEman MANager, provides a Python interface to
managing daemons running as system services. Daeman provides the
following API:

* start
* stop
* query status

A `status()` request can provide information about the process:

* name
* if it is running
* and process id

Currently, Systemd and Upstart are supported.


# Requirements

* System requirements: see ``requirements-system.csv``
* Python requirements: see ``requirements.txt``
* Development Python requirements: see ``requirements-devel.txt``


# Usage

For example, mange the SSH service on systemd:

```python
from daeman.initctl import Initctl
ssh = Initctl('ssh', sudo=True)
if not ssh.status().running:
    ssh.start()
status = ssh.status()
print status.name
print status.pid
```
