# Installation Guide

## Prerequisites

Before installing Touchpad, ensure you have:

- **Python 3.9** or higher
- **pip** package manager
- **Bluetooth adapter** on desktop (built-in or USB)
- **Mobile device** with Bluetooth (iOS 14+ or Android 9+)
- **Administrator/sudo access** (for some OS operations)

## Desktop Server Installation

### Windows

#### Step 1: Install Python

1. Download Python 3.9+ from [python.org](https://www.python.org)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   ```

#### Step 2: Clone Repository

```cmd
git clone https://github.com/yourusername/touchpad.git
cd touchpad
```

#### Step 3: Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 4: Install Dependencies

```cmd
pip install -r server\requirements.txt
```

#### Step 5: Configure Server

Copy and customize the configuration:

```cmd
copy server\config.ini server\config.local.ini
# Edit config.local.ini with your preferences
```

#### Step 6: Start Server

```cmd
python server\server.py --config server\config.local.ini
```

### macOS

#### Step 1: Install Python

Using Homebrew (recommended):

```bash
brew install python@3.11
```

Or download from [python.org](https://www.python.org)

#### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/touchpad.git
cd touchpad
```

#### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install -r server/requirements.txt
```

#### Step 5: Enable Bluetooth Permissions

```bash
# Grant Python permissions for Bluetooth
sudo chmod +x /usr/local/bin/python3
```

#### Step 6: Configure Server

```bash
cp server/config.ini server/config.local.ini
nano server/config.local.ini  # Edit as needed
```

#### Step 7: Start Server

```bash
python server/server.py --config server/config.local.ini
```

### Linux (Ubuntu/Debian)

#### Step 1: Install Python and Dependencies

```bash
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv
sudo apt-get install bluez python3-bluez libbluetooth-dev
sudo apt-get install xdotool  # For mouse control
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/touchpad.git
cd touchpad
```

#### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install -r server/requirements.txt
```

#### Step 5: Configure Bluetooth

```bash
# Start Bluetooth service
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER
# Log out and back in for group changes to take effect
```

#### Step 6: Configure Server

```bash
cp server/config.ini server/config.local.ini
nano server/config.local.ini  # Edit as needed
```

#### Step 7: Start Server

```bash
python server/server.py --config server/config.local.ini
```

### Linux (Fedora/RHEL)

```bash
# Install dependencies
sudo dnf install python3-devel bluez-libs python3-bluez
sudo dnf install xdotool

# Continue from Step 2 above
```

## Mobile Installation

### iOS

1. Open App Store
2. Search for "Touchpad Wireless Mouse"
3. Tap "Get" then "Install"
4. Grant permissions when prompted:
   - Bluetooth
   - Local Network
5. Launch the app

### Android

1. Open Google Play Store
2. Search for "Touchpad Wireless Mouse"
3. Tap "Install"
4. Grant permissions when prompted:
   - Bluetooth
   - Bluetooth Admin
   - Fine Location
5. Launch the app

## Verification

### Test Server Installation

```bash
# Discover available Bluetooth devices
python server/server.py --discover

# Expected output:
# Device name: MyComputer-Touchpad
# Listening on RFCOMM port 1
```

### Test Mobile App

1. Open Touchpad app on mobile
2. Tap "Scan for Devices"
3. Select your computer from the list
4. Confirm pairing request
5. Verify touchpad works

## Configuration

### Server Configuration File

Edit `server/config.ini`:

```ini
[bluetooth]
device_name = MyComputer-Touchpad  # Name shown in discovery
adapter = hci0                     # Bluetooth adapter (Linux)

[input]
mouse_speed = 1.5                 # Cursor speed multiplier
acceleration = true               # Enable acceleration
deadzone = 5                       # Dead zone in pixels

[logging]
level = INFO                       # Log level
file = touchpad.log               # Log file location
```

### Sensitivity Settings

- **mouse_speed**: 0.5 (slow) to 5.0 (fast), default 1.5
- **acceleration**: true/false, enables smooth acceleration
- **deadzone**: 0-50 pixels, ignore small movements

### Platform-Specific Notes

**Windows:**
- Requires administrator privileges for mouse input
- May need to disable Fast Startup for consistent behavior

**macOS:**
- Grant permissions in System Preferences > Security & Privacy
- May need to disable SIP (System Integrity Protection) for full functionality

**Linux:**
- User must be in bluetooth group
- xdotool required for mouse control
- May need to run with sudo if permissions insufficient

## Troubleshooting Installation

### "ModuleNotFoundError: No module named 'bluetooth'"

```bash
# Reinstall PyBluez
pip install --upgrade pybluez

# Or on macOS:
pip install pybluez --pre
```

### "Permission denied" errors

```bash
# Linux: Add to bluetooth group
sudo usermod -a -G bluetooth $USER
groups $USER  # Verify

# macOS: Grant permissions
sudo chmod +x /usr/local/bin/python3
```

### "Bluetooth adapter not found"

1. **Windows**: Check Device Manager for Bluetooth adapter
2. **macOS**: System Preferences > Bluetooth (enable)
3. **Linux**: `hciconfig` to list adapters

### "Connection refused"

1. Ensure server is running: `ps aux | grep server.py`
2. Check configuration
3. Restart Bluetooth service: `sudo systemctl restart bluetooth` (Linux)
4. Restart server

## Running as Service

### Linux (systemd)

Create `/etc/systemd/system/touchpad.service`:

```ini
[Unit]
Description=Touchpad Wireless Mouse Server
After=bluetooth.target
Wants=bluetooth.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/touchpad
ExecStart=/home/pi/touchpad/venv/bin/python /home/pi/touchpad/server/server.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable touchpad
sudo systemctl start touchpad
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\server\server.py`

## Uninstallation

### Complete Removal

```bash
# Stop server if running
# Remove directory
sudo rm -rf /path/to/touchpad

# Remove any created shortcuts
rm -rf ~/.local/share/applications/touchpad.desktop  # Linux
```

## Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for development setup
- Check [PROTOCOL.md](PROTOCOL.md) for protocol details
- See [../README.md](../README.md) for features overview
