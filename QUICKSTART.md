# Touchpad - Wireless Mouse Control via Bluetooth

A professional-grade, cross-platform wireless mouse control application that transforms your mobile device into a precision wireless touchpad.

## Quick Start

### Desktop Server

```bash
# Clone and setup
git clone https://github.com/yourusername/touchpad.git
cd touchpad
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install and run
pip install -r server/requirements.txt
python server/server.py
```

### Mobile App

Download from [App Store](link) or [Google Play](link), then connect to your computer.

## Key Features

✅ **Cross-Platform**: Windows, macOS, Linux  
✅ **Wireless**: Bluetooth RFCOMM connectivity  
✅ **Low Latency**: 50-150ms end-to-end response time  
✅ **Gestures**: Multi-touch gesture recognition  
✅ **Open Source**: MIT licensed, fully transparent  

## Documentation

- 📖 [Installation Guide](docs/SETUP.md)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)
- 📡 [Protocol Spec](docs/PROTOCOL.md)
- 🛠️ [Development Guide](docs/DEVELOPMENT.md)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)

## Technical Highlights

### Protocol
- Binary RFCOMM protocol with checksum validation
- 12+ message types for comprehensive control
- Variable-length payloads with size validation
- Backward compatible versioning

### Architecture
- Multi-threaded server
- Platform-agnostic input abstraction
- Mock device manager for testing
- Comprehensive logging system

### Quality
- 80%+ test coverage
- PEP 8 compliant code
- Type hints throughout
- CI/CD via GitHub Actions

## Requirements

- Python 3.9+
- Bluetooth adapter (desktop)
- iOS 14+ or Android 9+ (mobile)

## Performance

| Metric | Target |
|--------|--------|
| Latency | <100ms |
| Throughput | 60+ packets/s |
| Memory | <50MB |
| CPU | <5% idle |
| Battery | 4+ hrs |

## Installation

See [SETUP.md](docs/SETUP.md) for detailed platform-specific instructions.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT - See [LICENSE](LICENSE) for details

## Support

- 🐛 [Report Issues](https://github.com/yourusername/touchpad/issues)
- ✨ [Request Features](https://github.com/yourusername/touchpad/issues)
- 💬 [Discussions](https://github.com/yourusername/touchpad/discussions)

---

**Made with ❤️ by developers, for developers**
