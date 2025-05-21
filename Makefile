# Makefile for Whisper Local Transcribe

# Variables
PYTHON = python
SERVER_HOST = 0.0.0.0
SERVER_PORT = 8000
PYTEST = pytest
PIP = pip
DOCKER_COMPOSE = docker compose

# Default target
.PHONY: help
help:
	@echo "Whisper Local Transcribe"
	@echo ""
	@echo "Usage:"
	@echo "  make gui              Run the GUI client application"
	@echo "  make server           Run the API server"
	@echo "  make test             Run all tests"
	@echo "  make test-server      Run server tests"
	@echo "  make install          Install dependencies"
	@echo "  make docker-build     Build Docker images"
	@echo "  make docker-server    Start Docker server service"
	@echo "  make docker-down      Stop Docker services"
	@echo "  make docker-clean     Remove Docker containers, images, and volumes"
	@echo "  make clean            Remove generated files and directories"
	@echo "  make venv             Create and activate a virtual environment"

# Run the GUI application
.PHONY: gui
gui:
	@echo "Starting GUI application..."
	@$(PYTHON) app.py


# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

# Clean generated files and directories
.PHONY: clean
clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .pytest_cache -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@rm -rf uploads/*/*
	@mkdir -p uploads/transcriptions

.PHONY: venv
venv:
	@echo "Activating virtual environment..."
	@bash -c "source venv/bin/activate"