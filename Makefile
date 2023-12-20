SHELL := /bin/bash 

push: build ## build and push the module to pypi
	./.venv/bin/python -m twine upload --verbose ./dist/*

push-dev: build ## build and push the module to test pypi
	./.venv/bin/python -m twine upload --repository testpypi --verbose ./dist/*

build: pip-install-build ## compile/install all build dependencies and build the python pkg
	./.venv/bin/python -m build

pip-install-all: pip-compile pip-compile-dev pip-compile-build ## compile/install all dependencies
	pip install -r requirements.txt -r dev-requirements.txt -r build-requirements.txt

pip-install-build: pip-compile-build ## compile/install all build dependencies
	pip install -r build-requirements.txt

pip-install-dev: pip-compile-dev ## compile/install all dev dependencies
	pip install -r dev-requirements.txt

pip-install: pip-compile ## compile/install primary dependencies
	pip install -r requirements.txt

pip-compile-build: pip-tools ## compile build dependencies (build-requirements.txt)
	pip-compile --extra=build --output-file=build-requirements.txt pyproject.toml

pip-compile-dev: pip-tools ## compile dev dependencies (dev-requirements.txt)
	pip-compile --extra=dev --output-file=dev-requirements.txt pyproject.toml

pip-compile: pip-tools ## compile primary dependencies (requirements.txt)
	pip-compile

pip-tools: venv ## install pip-tools (pip-compile, pip-sync)
	pip install pip-tools

.PHONY: venv
venv: ## create and active venv in .venv
	python -m venv .venv

.PHONY: help
help: ## Print Makefile help
	@echo "Makefile usage:"
	@echo "  [INPUT_VARS] make <target>"
	@echo
	@if grep -qE '^.+ \?= .+$$' Makefile; then \
		echo "#### Input Variables ####"; \
	fi 
	@awk '$$1 ~ /^[A-Z]+/ && $$2 ~ /^\?=$$/ {gsub(/\?=./, "", $$0); gsub(/##/, "", $$2); $$2="(default: "$$2")"; printf "- %s \n", $$0}' Makefile
	@echo "#### Targets ####"
	@awk -F "##" '$$1 ~ /^[a-zA-Z-_]+:.*$$/ {gsub(":.*", "", $$1); printf "- %s:%s \n", $$1, $$2}' Makefile
