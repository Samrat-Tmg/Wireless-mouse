# Contributing to Touchpad

Thanks for your interest in contributing! Here's how you can help:

## Reporting Issues

Found a bug? Let us know! Include:
- What you were doing when it happened
- Your OS/Python version
- Error messages or logs
- Steps to reproduce

## Proposing Features

Have an idea? Open an issue describing:
- What the feature does
- Why it's useful
- How it might work

## Code Contributions

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `make test`
5. Commit with a clear message
6. Push and open a PR

### Keep in mind:
- Follow PEP 8 style guide
- Add tests for new features
- Update docs if needed
- One feature per PR

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/touchpad.git
cd touchpad

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r server/requirements.txt
pip install -r server/requirements-dev.txt
```

## Code Style

Follow PEP 8 - use black for formatting:
```bash
make format
```

## Testing & Quality

```bash
make test       # Run tests
make test-cov   # With coverage
make lint       # Check code quality
```

That's it! Thanks for contributing. 🙌
