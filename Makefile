SERVICES := edge-services notifications

# Where the built binaries end up (relative to the repo root)
BIN_DIR := bin

.PHONY: fmt check install venv build clean

fmt:
	ruff check --fix .
	ruff format .

check:
	ruff check .
	ruff format --check .

# Install requirements into each service's existing .venv (creates it if missing)
install:
	for d in $(SERVICES); do \
		( cd "$$d" && \
		  { [ -d .venv ] || python3 -m venv .venv; } && \
		  .venv/bin/pip install -r requirements.txt -r requirements-dev.txt ) || exit 1; \
	done

# Delete and recreate every .venv from scratch, then install
venv:
	for d in $(SERVICES); do rm -rf "$$d/.venv"; done
	$(MAKE) install

# Build a binary for every service via Docker + PyInstaller into $(BIN_DIR)/
build:
	for d in $(SERVICES); do \
		docker build -f "$$d/Dockerfile" --target export --output $(BIN_DIR) "$$d" || exit 1; \
	done

# Remove built binaries
clean:
	rm -rf $(BIN_DIR)