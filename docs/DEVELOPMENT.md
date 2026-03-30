# Development Guide

## Development Environment Setup

### Prerequisites

- Python 3.9+
- Git
- Code editor (VS Code, PyCharm, etc.)
- Familiarity with Bluetooth protocols (helpful)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/touchpad.git
cd touchpad

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies including dev tools
pip install -r server/requirements.txt
pip install -r server/requirements-dev.txt
```

## Code Structure

```
touchpad/
├── server/               # Desktop server
│   ├── server.py        # Main entry point
│   ├── device_manager.py # Bluetooth device management
│   ├── input_controller.py # OS-level input control
│   ├── config.py        # Configuration system
│   ├── __init__.py
│   ├── requirements.txt
│   └── config.ini       # Sample configuration
│
├── protocol/             # Communication protocol
│   ├── constants.py     # Protocol definitions
│   ├── serialization.py # Binary serialization
│   └── __init__.py
│
├── tests/               # Test suite
│   ├── test_protocol.py
│   ├── test_device_manager.py
│   └── __init__.py
│
├── docs/                # Documentation
│   ├── ARCHITECTURE.md
│   ├── PROTOCOL.md
│   ├── SETUP.md
│   └── DEVELOPMENT.md
│
└── .github/
    └── workflows/       # CI/CD pipelines
```

## Code Style

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points."""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# Bad
def calc_dist(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5
```

### Type Hints

Always use type hints:

```python
from typing import Optional, List, Dict

def process_devices(devices: List[str]) -> Dict[str, bool]:
    """Process devices and return status."""
    pass

def find_device(address: str) -> Optional[Device]:
    """Find device or return None."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def send_data(device_address: str, data: bytes) -> bool:
    """
    Send data to a connected device.
    
    Args:
        device_address: Bluetooth MAC address
        data: Data bytes to send
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        ValueError: If address format is invalid
        
    Example:
        >>> result = send_data("00:11:22:33:44:55", b"hello")
        >>> print(result)
        True
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_protocol.py -v

# Run with coverage
pytest --cov=server --cov=protocol --cov-report=html tests/

# Run specific test function
pytest tests/test_protocol.py::TestProtocolSerializer::test_cursor_move_encoding -v
```

### Writing Tests

```python
import unittest
from protocol.serialization import ProtocolSerializer

class TestProtocolSerializer(unittest.TestCase):
    """Test protocol serialization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.serializer = ProtocolSerializer()
    
    def test_cursor_move_encoding(self):
        """Test cursor move message encoding."""
        payload = ProtocolSerializer.encode_cursor_move(100, 200, 255)
        self.assertEqual(len(payload), 5)
    
    def tearDown(self):
        """Clean up after tests."""
        pass
```

### Test Coverage

Aim for >80% code coverage:

```bash
pytest --cov=server --cov=protocol --cov-report=term-missing tests/
```

## Code Quality Tools

### Formatting (Black)

```bash
# Format all Python files
black server/ protocol/ tests/

# Check formatting without changes
black --check server/
```

### Linting (Flake8)

```bash
# Run linter
flake8 server/ protocol/ tests/

# Configuration in .flake8:
# [flake8]
# max-line-length = 100
# ignore = E203, W503
```

### Type Checking (mypy)

```bash
# Run type checker
mypy server/ protocol/

# Strict mode
mypy --strict server/
```

### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

Install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

```bash
# Edit files
vim server/server.py

# Run tests
pytest tests/

# Format code
black server/

# Check types
mypy server/
```

### 3. Commit Changes

```bash
git add -A
git commit -m "Add new feature

This adds support for X feature. 

- Implemented Y
- Added tests for Z
- Updated documentation"
```

### 4. Push and Create PR

```bash
git push origin feature/my-feature
# Create PR on GitHub
```

## Adding New Features

### Adding a New Message Type

1. **Define constant in `protocol/constants.py`**:

```python
class MessageType:
    # ... existing types ...
    NEW_FEATURE = 0x10
```

2. **Add serialization in `protocol/serialization.py`**:

```python
@staticmethod
def encode_new_feature(param1: int, param2: str) -> bytes:
    """Encode new feature message."""
    return struct.pack('>H', param1) + param2.encode('utf-8')

@staticmethod
def decode_new_feature(payload: bytes) -> Optional[NewFeatureEvent]:
    """Decode new feature message."""
    if len(payload) < 2:
        return None
    # Parse and return
```

3. **Handle in server `server/server.py`**:

```python
elif msg_type == MessageType.NEW_FEATURE:
    event = ProtocolSerializer.decode_new_feature(payload)
    if event:
        self._handle_new_feature(event)
```

4. **Add tests in `tests/test_protocol.py`**:

```python
def test_new_feature_encoding(self):
    """Test new feature encoding."""
    payload = ProtocolSerializer.encode_new_feature(42, "test")
    self.assertIsNotNone(payload)
```

### Adding a New Configuration Option

1. **Add to default config in `server/config.py`**:

```python
def _set_defaults(self):
    # ... existing config ...
    self.config['features'] = {
        'new_option': 'default_value',
    }
```

2. **Add getter method**:

```python
def get_new_option(self) -> str:
    """Get new option value."""
    return self.config.get('features', 'new_option', fallback='default_value')
```

3. **Use in code**:

```python
value = self.config.get_new_option()
```

## Debugging

### Enable Debug Logging

```bash
python server/server.py --debug
```

### Using pdb

```python
import pdb

# Set breakpoint
pdb.set_trace()

# Commands:
# n - next line
# s - step into
# c - continue
# p <var> - print variable
# l - list code
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

Adjust log level in `server/config.ini`:

```ini
[logging]
level = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Performance Profiling

### CPU Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
# ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Memory Profiling

```bash
pip install memory-profiler

python -m memory_profiler server/server.py
```

## Documentation

### Updating Documentation

1. Edit markdown files in `docs/`
2. Build HTML (optional):

```bash
pip install mkdocs
mkdocs build
```

3. Preview locally:

```bash
mkdocs serve
```

## Release Process

### Version Numbering

Use [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

### Creating a Release

1. Update version in relevant files
2. Update CHANGELOG
3. Create git tag:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

4. Create release on GitHub with release notes

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Resources

- [Python Documentation](https://docs.python.org/)
- [Bluetooth SIG](https://www.bluetooth.org/)
- [PyBluez Documentation](https://github.com/pybluez/pybluez)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Testing Best Practices](https://docs.pytest.org/)

## Troubleshooting Development

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall in development mode
pip install -e .
```

### Test Failures

```bash
# Run with verbose output
pytest test_file.py::test_function -vv

# Show local variables on failure
pytest --showlocals test_file.py

# Stop on first failure
pytest -x test_file.py
```

### Bluetooth Issues

```bash
# List connected devices
python server/server.py --discover

# Enable mock mode for testing without hardware
python server/server.py --mock
```
