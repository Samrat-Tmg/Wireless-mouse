# Project Copilot Instructions

## Project Context

**Touchpad** is a professional-grade wireless mouse control application that allows users to control their desktop computer's mouse using their mobile device via Bluetooth. The project is designed for Windows, macOS, and Linux, with companion apps for iOS and Android.

## Architecture Summary

The project follows a client-server architecture:

- **Server (Desktop)**: Python-based backend handling Bluetooth connections, device management, and OS-level input control
- **Protocol**: Custom binary protocol over Bluetooth RFCOMM for efficient communication
- **Mobile Clients**: Native iOS and Android apps (codebases separate)

## Key Modules

### Server Package (`server/`)
- **server.py**: Main entry point, connection handler, and message router
- **device_manager.py**: Bluetooth device discovery, pairing, and connection management
- **input_controller.py**: Cross-platform OS input simulation (Windows, macOS, Linux)
- **config.py**: Configuration file parsing and management

### Protocol Package (`protocol/`)
- **constants.py**: Message types, protocol definitions, and constants
- **serialization.py**: Binary packet encoding/decoding with checksum validation

### Testing (`tests/`)
- Unit tests for protocol and device management
- Mock device manager for testing without Bluetooth hardware

### Documentation (`docs/`)
- ARCHITECTURE.md: System design and data flow
- PROTOCOL.md: Binary protocol specification
- SETUP.md: Installation and configuration instructions
- DEVELOPMENT.md: Development environment and contributing guidelines
- TROUBLESHOOTING.md: Common issues and solutions

## Code Style

- **Python**: PEP 8 compliant with 100-char line limit
- **Type Hints**: Required throughout codebase
- **Docstrings**: Google-style docstrings for all public APIs
- **Testing**: 80%+ code coverage with pytest
- **Linting**: Flake8 and MyPy with pre-commit hooks

## Development Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and run tests: `pytest tests/ -v`
3. Format code: `black server/ protocol/`
4. Type check: `mypy server/ protocol/`
5. Commit with clear message: `git commit -m "Feature: description"`
6. Create pull request with changelog entry

## Key Implementation Details

### Binary Protocol
- Message format: `[Magic 0xAD][Type][Length][Payload][XOR Checksum]`
- Supports 12 message types (cursor move, clicks, scroll, gestures, etc.)
- Variable-length payloads with size validation
- Checksum-based error detection

### Cross-Platform Input
- Windows: ctypes + Win32 API (SetCursorPos, mouse_event)
- macOS: Quartz framework (CGEvent functions)
- Linux: xdotool command-line tool

### Device Management
- Bluetooth RFCOMM socket-based communication
- Mock device manager for testing
- Connection timeout and keep-alive mechanisms
- Thread-safe device operations

## Important Constraints

1. **No AI/ML**: All code should appear human-written, avoiding overly sophisticated patterns
2. **Performance**: Maintain <100ms latency for cursor movement
3. **Windows/Mac/Linux**: Full cross-platform support required
4. **Bluetooth**: Standard BLE/RFCOMM only, no vendor-specific extensions
5. **Security**: Standard Bluetooth pairing, no custom encryption

## Common Tasks

### Adding New Message Type
1. Add constant in `protocol/constants.py`
2. Implement encoder/decoder in `protocol/serialization.py`
3. Handle in `server/server.py` message router
4. Add tests in `tests/test_protocol.py`

### Adding Configuration Option
1. Add to defaults in `server/config.py`
2. Create getter method
3. Document in `server/config.ini`
4. Use in appropriate module

### Fixing Cross-Platform Issue
1. Check implementation in `server/input_controller.py`
2. Fix appropriate subclass (Windows/macOS/Linux)
3. Test on relevant OS
4. Update TROUBLESHOOTING.md if user-facing

## Testing Strategy

- Unit tests for low-level components (protocol, config)
- Integration tests for device manager
- Mock-based testing for Bluetooth without hardware
- Run with: `pytest tests/ -v --cov=server --cov=protocol`

## Documentation

- Keep docs up-to-date with code changes
- Use Markdown for all documentation
- Include code examples where relevant
- Update CHANGELOG.md for all significant changes

## Build and Release

- Semantic versioning (MAJOR.MINOR.PATCH)
- Version bumps in setup files and code
- Git tags for releases: `git tag -a v1.0.0`
- GitHub releases with comprehensive notes
- CI/CD via GitHub Actions (tests, security checks)

## Performance Targets

- Cursor latency: <100ms
- Throughput: 60+ packets/second
- Memory: <50MB
- CPU: <5% idle, <20% active
- Battery: 4+ hours on mobile

## Security Considerations

- Use standard Bluetooth pairing
- Validate all packet checksums
- Input boundary checking
- No sensitive data in logs
- Regular dependency updates

## Files to Modify Often

- `server/server.py`: New features, handlers
- `protocol/constants.py`: New message types
- `protocol/serialization.py`: Protocol changes
- `server/config.py`: Configuration options
- `docs/CHANGELOG.md`: All changes

## Files to Touch Rarely

- `server/input_controller.py`: Only for OS-specific fixes
- `device_manager.py`: Core architecture changes
- Protocol format: Maintains compatibility

## Getting Help

- Check [DEVELOPMENT.md](docs/DEVELOPMENT.md) for setup
- Review [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues
- See [PROTOCOL.md](docs/PROTOCOL.md) for protocol questions
- Check existing GitHub issues before creating new

## Key Contacts & Resources

- Python docs: https://docs.python.org/
- Bluetooth SIG: https://www.bluetooth.org/
- PyBluez: https://github.com/pybluez/pybluez
- PEP 8: https://www.python.org/dev/peps/pep-0008/
