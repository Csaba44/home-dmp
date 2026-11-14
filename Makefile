.PHONY: fmt check

fmt:
	ruff check --fix .
	ruff format .

check:
	ruff check .
	ruff format --check .
