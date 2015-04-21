
NAME=daeman
VENV=venv/$(NAME)
PIP_INSTALL=pip install
PIP_INSTALL_REQ=$(PIP_INSTALL) -r

.PHONY: main
main: install

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
devel: requirements-devel.txt pip-update
	$(PIP_INSTALL_REQ) $<

.PHONY: test
test: setup.py
	python $< nosetests -s

.PHONY: install
install: setup.py depends
	python $< install


.PHONY: venv
venv:
	if [[ ! -d $(VENV) ]]; then \
	    virtualenv $(VENV);\
	fi ;\
	source $(VENV)/bin/activate
	pip install -U pip


.PHONY: vagrant
vagrant:
	vagrant up --provider=virtualbox
