.PHONY: install test lint run 

help:
	@echo "test - run unit tests"
	@echo "lint - run linter and checks"

test:
	poetry run pytest -vv test

check:
	./static_checks.sh

lint:
	./linter.sh