# ==============================================
# Project: knight-journey
# Makefile (compatible with src/ layout)
# ==============================================

# ---------- Configuration ----------
SHELL := /bin/bash
.DEFAULT_GOAL := help

VENV ?= .venv
PY ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip

PKG_NAME ?= knight_journey
CLI_NAME ?= knight-journey

INPUT_FILE ?= input.yaml

# Pytest/Coverage flags
PYTEST_FLAGS ?= -q
COV_FLAGS ?= --cov=$(PKG_NAME) --cov-report=term-missing --cov-report=xml

# Docker configuration
DOCKER ?= docker
IMAGE ?= knight-journey
TAG ?= latest
PY_VER ?= 3.13


# ---------- Help ----------
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  setup            Create virtual environment and install package (editable)"
	@echo "  setup-dev        setup + install dev tools (pytest, black, ruff, etc.)"
	@echo "  test             Run tests with coverage"
	@echo "  run              Run the app using 'python -m $(PKG_NAME)'"
	@echo "  cli              Run the CLI entry point ($(CLI_NAME))"
	@echo "  format           Run Black code formatter"
	@echo "  lint             Run Ruff linter"
	@echo "  check            Run lint + tests"
	@echo "  dist             Build sdist & wheel distributions"
	@echo "  clean            Remove caches and build artifacts"
	@echo "  deep-clean       Clean + remove virtual environment"
	@echo ""
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run CLI inside Docker (with mounted input.yaml)"
	@echo "  docker-test      Run pytest inside Docker"
	@echo "  docker-shell     Open interactive bash shell inside Docker"
	@echo "  docker-clean     Remove Docker image"
	@echo "  docker-push      Push Docker image to registry"
	@echo ""
	@echo "Variables (can be overridden with VAR=value):"
	@echo "  VENV=$(VENV)  PY=$(PY)  PIP=$(PIP)"
	@echo "  IMAGE=$(IMAGE)  TAG=$(TAG)  PY_VER=$(PY_VER)"
	@echo "  INPUT_FILE=$(INPUT_FILE)"
	@echo ""
	@echo "Examples:"
	@echo "  make setup-dev"
	@echo "  make test"
	@echo "  make run INPUT_FILE=./input.yaml"
	@echo "  make docker-build IMAGE=$(IMAGE) TAG=dev PY_VER=$(PY_VER)"
	@echo "  make docker-run IMAGE=$(IMAGE) TAG=dev"


# ---------- Python environment ----------
$(VENV)/bin/activate: | $(VENV)
	@true

$(VENV):
	python3 -m venv $(VENV)

.PHONY: setup
setup: $(VENV)
	$(PIP) install -U pip
	$(PIP) install -e .

.PHONY: setup-dev
setup-dev: setup
	# Install common dev tools
	$(PIP) install pytest pytest-cov black ruff


# ---------- Testing & execution ----------
.PHONY: test
test:
	$(PY) -m pytest $(PYTEST_FLAGS) $(COV_FLAGS)

.PHONY: run
run:
	$(PY) -m $(PKG_NAME) --input $(INPUT_FILE)

.PHONY: cli
cli:
	# Requires [project.scripts] section in pyproject.toml
	$(CLI_NAME) --input $(INPUT_FILE)


# ---------- Code quality ----------
.PHONY: format
format:
	$(VENV)/bin/black src tests

.PHONY: lint
lint:
	$(VENV)/bin/ruff check src tests

.PHONY: check
check: lint test


# ---------- Build & clean ----------
.PHONY: dist
dist:
	rm -rf dist build *.egg-info src/*.egg-info
	$(PY) -m pip install -U build
	$(PY) -m build

.PHONY: clean
clean:
	rm -rf .pytest_cache .coverage coverage.xml build dist \
	       *.egg-info src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: deep-clean
deep-clean: clean
	rm -rf $(VENV)


# ---------- Docker section ----------
.PHONY: docker-build
docker-build:
	DOCKER_BUILDKIT=1 $(DOCKER) build \
		--build-arg PY_VER=$(PY_VER) \
		-t $(IMAGE):$(TAG) .

.PHONY: docker-run
docker-run:
	# Run CLI inside container using mounted input.yaml
	$(DOCKER) run --rm -it \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE):$(TAG) \
		python -m $(PKG_NAME) --input /app/$(INPUT_FILE)

.PHONY: docker-test
docker-test:
	# Run pytest inside container
	$(DOCKER) run --rm -it \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE):$(TAG) \
		pytest $(PYTEST_FLAGS) $(COV_FLAGS)

.PHONY: docker-shell
docker-shell:
	# Open interactive bash shell
	$(DOCKER) run --rm -it \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE):$(TAG) \
		bash

.PHONY: docker-clean
docker-clean:
	-$(DOCKER) rmi $(IMAGE):$(TAG) 2>/dev/null || true

.PHONY: docker-push
docker-push:
	$(DOCKER) push $(IMAGE):$(TAG)
