PROJECT = sreport
DESCRIPTION = A Python program to make HTTP(S) requests and report on the results
BOLD :=  $(shell tput bold)
RESET :=  $(shell tput sgr0)

help: ## This 'help' documentation
	@printf "$(BOLD)$(PROJECT): $(RESET)$(DESCRIPTION)\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BOLD)%-24s\033[0m $(RESET)%s\n", $$1, $$2}' | sort

requirements:  ## Install dependencies required to run and test this script
	pip3 install -r requirements.txt

test:  ## Run unit tests and code style checks
	@printf "$(BOLD)Running pycodestyle...$(RESET)\n"
	find . -name '*.py' -exec pycodestyle {} +;

	@printf "\n$(BOLD)Running pylint...$(RESET)\n"
	find . -name '*.py' -exec pylint {} +;

	@printf "\n$(BOLD)Running unit tests (py.test)$(RESET)\n"
	py.test tests

dockertest:  ## Build and run tests inside a Docker container
	docker build . --tag $(PROJECT):latest
	docker run -t --rm $(PROJECT):latest

.PHONY: help init test
