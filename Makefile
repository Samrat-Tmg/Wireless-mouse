.PHONY: help install install-dev lint format test test-cov clean run discover debug

help:
	@echo "Touchpad Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies"
	@echo "  make install-dev   Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make lint          Run linters (flake8, mypy)"
	@echo "  make format        Format code (black)"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo ""
	@echo "Running:"
	@echo "  make run           Start server"
	@echo "  make debug         Start server in debug mode"
	@echo "  make discover      Discover Bluetooth devices"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         Clean build artifacts"

install:
	pip install -r server/requirements.txt

install-dev:
	pip install -r server/requirements.txt
	pip install -r server/requirements-dev.txt

lint:
	flake8 server/ protocol/ tests/
	mypy server/ protocol/

format:
	black server/ protocol/ tests/
	isort server/ protocol/ tests/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=server --cov=protocol --cov-report=html --cov-report=term-missing

run:
	python server/server.py --config server/config.ini

debug:
	python server/server.py --debug --log-level DEBUG --config server/config.ini

discover:
	python server/server.py --discover

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	rm -f htmlcov/index.html 2>/dev/null || true
	@echo "Cleaned!"
