#
# Project:   snaps
# Copyright: (c) 2020 Tyler Mulligan - all rights reserved
#
# A GNU Makefile for the project.
#

.PHONY: help clean develop install lint security tests tests-coverage version

help:
	@echo "Use \`make <target>', where <target> is one of the following:"
	@echo "  clean              - remove all generated files"
	@echo "  develop            - install the python package, dev dependencies, and setup in develop mode"
	@echo "  docs               - build the documentation"
	@echo "  docs-serve         - build the documentation and serve it with python's http server"
	@echo "  install            - install the python package"
	@echo "  lint               - check code style with flake8"
	@echo "  security           - run security scans"
	@echo "  tests              - run tests"
	@echo "  tests-coverage     - obtain test coverage"

clean:
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.py[co]' -exec rm -f {} +
	@rm -rf .tox

develop:
	$(MAKE) install && pip3 install -r requirements-dev.in

install:
	@pip3 install -e .

lint:
	@flake8

security:
	@bandit -r --ini .bandit || exit 1
	@pip3 freeze | safety check --stdin

tests:
	@pytest

tests-coverage:
	@tox
