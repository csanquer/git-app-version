# set default shell
SHELL := $(shell which bash)
# default shell options
.SHELLFLAGS = -c

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
PYTHON_REQUIREMENTS_DEV_FILE ?= requirements-dev.txt
# QUICK ?=
VIRTUAL_ENV ?= .virtualenv-$(PYTHON_BASENAME)
PIP ?= $(VIRTUAL_ENV)/bin/pip
PYTEST ?= $(VIRTUAL_ENV)/bin/pytest
PYTEST_OPTIONS ?= --capture=no --cov=git_semver --cov-report html

.SILENT: ;               # no need for @
.ONESHELL: ;             # recipes execute in same shell
.NOTPARALLEL: ;          # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell
default: all;   # default target

.PHONY: all

all: install install-dev lint lint-html test

# Setup the local virtualenv, or use the one provided by the current environment.
$(VIRTUAL_ENV):
	virtualenv -p $(PYTHON) $(VIRTUAL_ENV)
	$(PIP) install -U pip wheel
	ln -fs $(VIRTUAL_ENV)/bin/activate activate-$(PYTHON_BASENAME)

install: $(VIRTUAL_ENV)
	$(PIP) install -r $(PYTHON_REQUIREMENTS_FILE)

install-dev: $(VIRTUAL_ENV)
	$(PIP) install -r $(PYTHON_REQUIREMENTS_DEV_FILE)

lint: install-dev
	$(VIRTUAL_ENV)/bin/pylint git_app_version -f colorized

lint-html: install-dev
	$(VIRTUAL_ENV)/bin/pylint git_app_version -f html > pylint.html

lint3: install-dev
	$(VIRTUAL_ENV)/bin/pylint --py3k git_app_version -f colorized

lint3-html: install-dev
	$(VIRTUAL_ENV)/bin/pylint --py3k git_app_version -f html > pylint.html

test:
	$(VIRTUAL_ENV)/bin/coverage erase
	$(VIRTUAL_ENV)/bin/coverage run -m py.test
	$(VIRTUAL_ENV)/bin/coverage report -m
	$(VIRTUAL_ENV)/bin/coverage html
	$(VIRTUAL_ENV)/bin/coverage xml

test-all:
	tox --skip-missing-interpreters
