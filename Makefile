
NAME=daeman
VENV=venv/$(NAME)
PIP_INSTALL=pip install
PIP_INSTALL_REQ=$(PIP_INSTALL) -r

.PHONY: main
main: install

.PHONY: venv
venv:
	if [[ ! -d $(VENV) ]]; then \
	    virtualenv $(VENV);\
	fi ;\
	source $(VENV)/bin/activate


.PHONY: pip-update
pip-update:
	$(PIP_INSTALL) -U pip


.PHONY: depends
depends: requirements.txt pip-update
	$(PIP_INSTALL_REQ) $<


.PHONY: depends-upgrade
depends-upgrade: requirements.txt pip-update
	$(PIP_INSTALL_REQ) $< -U


.PHONY: devel
devel: requirements-devel.txt depends pip-update
	$(PIP_INSTALL_REQ) $<


.PHONY: test-systemd
test-systemd: setup.py
	python $< nosetests -s -A 'not service == "upstart"'

.PHONY: test-upstart
test-upstart: setup.py
	python $< nosetests -s -A 'not service == "systemd"'


.PHONY: install
install: setup.py depends
	python $< install


.PHONY: vagrant
vagrant:
	vagrant up --provider=virtualbox
