.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: init test  ## Initiate all tests

.PHONY: init
init: ## Installs the develop tools and runs the coverage
	python setup.py develop
	pip install tox "coverage<5"

.PHONY: test
test: ## Runs the tests
	coverage erase
	tox --parallel--safe-build
	coverage html

.PHONY: serve-docs
serve-docs: ## Runs the local docs
	mkdocs serve

.PHONY: build-docs
build-docs: ## Runs the local docs
	mkdocs build

ifndef VERBOSE
.SILENT:
endif
