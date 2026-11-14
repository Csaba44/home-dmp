SERVICES := edge-services notifications

.PHONY: fmt check install venv

fmt:
	ruff check --fix .
	ruff format .

check:
	ruff check .
	ruff format --check .

install:
	for d in $(SERVICES); do \
		( cd "$$d" && \
		  { [ -d .venv ] || python3 -m venv .venv; } && \
		  .venv/bin/pip install -r requirements.txt -r requirements-dev.txt ) || exit 1; \
	done

venv:
	for d in $(SERVICES); do rm -rf "$$d/.venv"; done
	$(MAKE) install