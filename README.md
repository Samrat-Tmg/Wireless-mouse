# Touchpad

Control your desktop mouse from your phone via Bluetooth. Works on Windows, macOS, and Linux.

## Features

- Cross-platform (Windows, macOS, Linux)
- Bluetooth connectivity
- Real-time cursor control
- Multi-touch gestures
- Click and scroll support
- Low latency (~100ms)

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/touchpad.git
cd touchpad
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r server/requirements.txt

# Run server (mock mode for testing)
python server/server.py --mock

# Or with real Bluetooth
python server/server.py
```

Install the mobile app (iOS/Android) from the companion repositories, then connect to your computer running this server.

See [SETUP.md](docs/SETUP.md) for detailed platform-specific instructions.

## How It Works

Mobile app sends touch coordinates over Bluetooth RFCOMM. Server translates them to mouse movements on your desktop.

## Project Layout

```
touchpad/
├── server/           # Desktop server
├── protocol/         # Bluetooth protocol
├── tests/           # Unit tests
└── docs/            # Documentation
```

## Documentation

- [Setup](docs/SETUP.md) - Installation for all platforms
- [Protocol](docs/PROTOCOL.md) - How the protocol works
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Development](docs/DEVELOPMENT.md) - Contributing guide
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## Development

```bash
make test       # Run tests
make lint       # Check code quality
make format     # Format code
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - see [LICENSE](LICENSE)
