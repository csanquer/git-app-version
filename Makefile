# set default shell
SHELL := $(shell which bash)
# default shell options
.SHELLFLAGS = -c

APP_NAME=git-app-version
SRC_DIR=git_app_version
TEST_DIR=tests

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
PYTHON_REQUIREMENTS_DEV_FILE ?= requirements-dev.txt
# QUICK ?=
VENV ?= .virtualenv-$(PYTHON_BASENAME)
BIN_DIR ?= $(VENV)/bin
PIP ?= $(BIN_DIR)/pip
PYTEST ?= $(BIN_DIR)/pytest
PYTEST_OPTIONS ?= --capture=no --cov=git_semver --cov-report html

.SILENT: ;               # no need for @
.ONESHELL: ;             # recipes execute in same shell
.NOTPARALLEL: ;          # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell
default: all;   # default target

.PHONY: all

all: install install-dev lint lint-html test

# Setup the local virtualenv, or use the one provided by the current environment.
$(VENV):
	virtualenv -p $(PYTHON) $(VENV)
	$(PIP) install -U pip wheel
	ln -fs $(BIN_DIR)/activate activate-$(PYTHON_BASENAME)

install: $(VENV)
	$(PIP) install versioneer
	$(PIP) install pypandoc
	$(PIP) install -r $(PYTHON_REQUIREMENTS_FILE)

install-dev: $(VENV)
	$(PIP) install versioneer
	$(PIP) install pypandoc
	$(PIP) install -r $(PYTHON_REQUIREMENTS_DEV_FILE)

# Python coding standards
yapf:
	$(BIN_DIR)/yapf --in-place -r $(SRC_DIR) $(TEST_DIR)

pep8:
	$(BIN_DIR)/pep8 $(SRC_DIR) $(TEST_DIR)

flake8:
	$(BIN_DIR)/flake8 $(SRC_DIR) $(TEST_DIR)

isort:
	$(BIN_DIR)/isort -rc $(SRC_DIR) $(TEST_DIR)

lint:
	$(BIN_DIR)/pylint $(SRC_DIR) -f colorized || exit 0

lint-html:
	$(BIN_DIR)/pylint $(SRC_DIR) -f html > pylint.html || exit 0

lint3:
	$(BIN_DIR)/pylint --py3k $(SRC_DIR) -f colorized || exit 0

lint3-html:
	$(BIN_DIR)/pylint --py3k $(SRC_DIR) -f html > pylint.html || exit 0

compile:
	git describe --tags --always > $(SRC_DIR)/version.txt
	$(BIN_DIR)/pyinstaller -D $(APP_NAME).spec
	rm -f $(SRC_DIR)/version.txt

# $(TEST_DIR)
test:
	$(PYTEST) --cov=git_app_version \
	--no-cov-on-fail \
	--cov-report term-missing \
	--cov-report html \
	--cov-report xml

test-all:
	$(BIN_DIR)/tox --skip-missing-interpreters

test-23:
	$(BIN_DIR)/tox -e py27,py35
