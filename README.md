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


# Developing

If you would like to develop on Daeman, first checkout the code:

```
$ git clone git@github.com:badi/daeman.git
$ cd daeman
```

Examine the ``requirements-system.csv`` file to make sure you have the
appropriate packages install. If you happen to be on Ubuntu 14.04 you may execute the following:

```
$ cut -d, -f1 requirements-system.csv | tail -n +2 | xargs sudo apt-get install
```

We recommend you develop in a virtual environment.
A Makefile rule is provided that will create one for you:

```
$ make venv
```

Now activate it:

```
$ source venv/daeman/bin/activate
```

To install python dependencies for development:

```
$ make devel
```

For testing: use `make test-systemd` or `make test-upstart` as appropriate.
Vagrant may also be used for testing upstart:

```
$ vagrant up
$ vagrant ssh
$ cd /code
$ make test-upstart
```
