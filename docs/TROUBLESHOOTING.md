# Troubleshooting Guide

## Common Issues and Solutions

### Connection Issues

#### "No Bluetooth Adapter Found"

**Symptoms**: Server starts but cannot scan for devices.

**Solutions**:

**Windows:**
1. Check Device Manager:
   - Press `Win + X` → Device Manager
   - Look for "Bluetooth"
   - If missing, install Bluetooth drivers
2. Enable Bluetooth in Settings:
   - Settings → Devices → Bluetooth & devices
3. If using USB adapter:
   - Plug in the adapter
   - Install drivers from manufacturer

**macOS:**
1. System Preferences → Bluetooth
2. If grayed out, restart the system
3. Reset NVRAM: Power on, hold `Cmd + Option + P + R` until Apple logo appears twice

**Linux:**
1. Check adapter:
   ```bash
   hciconfig
   # Should show hci0, hci1, etc. as UP/DOWN
   ```
2. Enable if down:
   ```bash
   sudo hciconfig hci0 up
   ```
3. Check BlueZ service:
   ```bash
   sudo systemctl status bluetooth
   sudo systemctl start bluetooth
   ```

#### "Mobile Won't Connect"

**Symptoms**: Server running, but mobile device cannot find or connect.

**Solutions**:
1. **Restart both devices**
   - Disconnect and restart server
   - Restart mobile device's Bluetooth
   
2. **Verify server is advertising**
   ```bash
   python server/server.py --discover
   # Should find devices
   ```

3. **Check permissions on mobile**
   - iOS: Settings → Touchpad → Bluetooth
   - Android: Settings → Apps → Touchpad → Permissions → Enable all

4. **Move closer to server**
   - Reduce distance between devices
   - Bluetooth range is ~10 meters

5. **Forget and re-pair**
   - Mobile: Settings → Bluetooth → Forget device
   - Server: Delete pairing file (varies by OS)
   - Try pairing again

#### "Connection Drops Frequently"

**Symptoms**: Frequent disconnects, "Device not responding"

**Solutions**:
1. **Check interference**
   - Move away from WiFi routers, microwaves
   - These use 2.4 GHz like Bluetooth
   
2. **Update firmware**
   - Check for Bluetooth driver/firmware updates
   
3. **Increase keep-alive timeout in config.ini**:
   ```ini
   [network]
   timeout = 60  # Increase from 30
   ```

4. **Reduce other Bluetooth devices**
   - Disconnect other devices
   - Test with only server and mobile

5. **Check battery**
   - Ensure mobile has sufficient battery
   - Low battery can cause connection issues

### High Latency / Slow Response

**Symptoms**: Cursor response delayed, lag when moving

**Solutions**:
1. **Reduce distance** between devices
2. **Disable acceleration** temporarily to test:
   ```ini
   [input]
   acceleration = false
   ```
3. **Reduce update frequency** (in mobile app settings)
4. **Check CPU usage**:
   - Server using >50% CPU?
   - Reduce log level to INFO

### Input Not Working

#### "Server Running But Mouse Won't Move"

**Windows:**
1. Run as Administrator
2. Verify permissions:
   ```cmd
   python server/server.py --debug
   ```
3. Check if UAC blocking:
   - Disable UAC temporarily to test
   - Control Panel → User Accounts → UAC

**macOS:**
1. Grant permissions:
   - System Preferences → Security & Privacy
   - Allow Python/Terminal
2. May need to disable SIP (System Integrity Protection):
   ```bash
   csrutil disable
   ```

**Linux:**
1. Check xdotool installed:
   ```bash
   which xdotool
   ```
2. If not installed:
   ```bash
   sudo apt-get install xdotool  # Ubuntu/Debian
   sudo dnf install xdotool      # Fedora
   ```
3. Check user permissions:
   ```bash
   groups
   # Should include 'input' group
   sudo usermod -a -G input $USER
   ```

#### "Clicks Work But Not All"

**Solutions**:
1. Check mouse speed config:
   ```ini
   [input]
   mouse_speed = 1.5
   ```
   Try adjusting to 1.0 then 2.0

2. Verify deadzone setting:
   ```ini
   deadzone = 5  # Increase if very sensitive
   ```

3. Check for double-click interference:
   ```ini
   # In server, disable double-click feature if not needed
   ```

### Installation Issues

#### "pip install fails with error"

**Solution 1: Update pip, setuptools, wheel**
```bash
pip install --upgrade pip setuptools wheel
```

**Solution 2: Install specific version**
```bash
pip install pybluez==0.23
pip install pynput==1.7.6
```

**Solution 3: Use pre-built wheels** (on Windows)
```bash
# Download wheels from pypi.org
# Place in same directory
pip install *.whl
```

#### "ModuleNotFoundError: blah blah"

```bash
# Verify virtual environment is active
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r server/requirements.txt

# Check installed packages
pip list
```

#### "Permission denied: config.ini"

```bash
# Fix permissions
chmod 644 server/config.ini

# Or run with sudo (not recommended)
sudo python server/server.py
```

### Bluetooth Specific

#### "PyBluez ImportError on macOS"

```bash
# Try pre-built wheel
pip install pybluez --pre

# Or compile from source
pip install --upgrade pybluez --no-binary :all:
```

#### "hciconfig command not found" (Linux)

```bash
sudo apt-get install bluez
sudo apt-get install libbluetooth-dev
```

#### "rfcomm: error: device or resource busy"

```bash
# Kill existing connections
sudo rfcomm release all

# Or restart service
sudo systemctl restart bluetooth
```

### Performance Issues

#### "High CPU Usage"

**Causes & Solutions**:
1. **Debug logging enabled**
   ```ini
   [logging]
   level = INFO  # Not DEBUG
   ```

2. **Update frequency too high**
   - Reduce in mobile app settings
   - Target 30-60 Hz

3. **Too many connected devices**
   - Limit in config:
   ```ini
   [network]
   max_connections = 5
   ```

#### "High Memory Usage"

**Causes & Solutions**:
1. **Large log files**
   - Configure rotation:
   ```ini
   [logging]
   max_size = 10485760  # 10MB
   backup_count = 3
   ```

2. **Many devices accumulated**
   - Restart server to clear cache

3. **Memory leak**
   - Check for recent changes
   - Revert and test

### Configuration Issues

#### "Config file not found"

```bash
# Verify file exists
ls -la server/config.ini  # Linux/macOS
dir server\config.ini      # Windows

# If missing, copy sample
cp server/config.ini.sample server/config.ini
```

#### "Invalid configuration value"

```ini
# Common mistakes:
mouse_speed = "1.5"   # Wrong: quoted
mouse_speed = 1.5    # Correct

acceleration = True   # Wrong: capital T
acceleration = true   # Correct
```

Restart server after editing config:
```bash
python server/server.py --config server/config.local.ini
```

### Mobile App Specific

#### "App Crashes on Launch"

**iOS:**
1. Force close app: Swipe up
2. Clear cache: Settings → General → iPhone Storage
3. Reinstall: Delete and re-download from App Store

**Android:**
1. Clear cache: Settings → Apps → Touchpad → Storage → Clear Cache
2. Clear data: Storage → Clear Data
3. Force stop and restart

#### "Can't Find Server Even Though It's Running"

1. **Verify server is advertising**
   - Open server debug info
   - Should show "Advertising..." or "Listening..."

2. **Check Bluetooth on mobile**
   - iPhone: Settings → Bluetooth (ON)
   - Android: Settings → Connected Devices → Bluetooth (ON)

3. **Restart mobile Bluetooth**
   - iPhone: Settings → Bluetooth → toggle OFF/ON
   - Android: Airplane mode ON/OFF

### Testing with Mock Mode

If Bluetooth hardware not available:

```bash
# Use mock device manager
python server/server.py --mock --debug
```

This simulates Bluetooth without requiring hardware.

### Collecting Debug Information

When reporting issues, collect:

```bash
# System info
python --version
pip list

# Bluetooth devices (if available)
python server/server.py --discover

# Debug log
python server/server.py --debug 2>&1 | tee debug.log

# Connection test
python server/server.py --config server/config.ini

# OS info
uname -a        # Linux/macOS
systeminfo      # Windows
```

### Getting Help

1. **Check logs**:
   ```bash
   tail -f touchpad.log
   ```

2. **Enable debug mode**:
   ```bash
   python server/server.py --debug --log-level DEBUG
   ```

3. **Search GitHub issues**:
   - May already be reported
   - Search by error message

4. **Create bug report** with:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Debug logs
   - System information

5. **Contact support**:
   - GitHub Issues
   - Email: support@example.com

## Advanced Troubleshooting

### Bluetooth Protocol Analyzer

```bash
# Linux: Use hcidump
sudo hcidump -i hci0 -t -A

# macOS: Bluetooth Explorer (included with Additional Tools)
```

### System Logs

**Windows:**
- Event Viewer → Windows Logs → System
- Filter by errors

**macOS:**
```bash
grep -i bluetooth /var/log/system.log
```

**Linux:**
```bash
journalctl -u bluetooth -f
```

### Performance Monitoring

**Linux/macOS:**
```bash
top -p $(pgrep -f server.py)
```

**Windows:**
- Task Manager → Performance tab

## Emergency Procedures

### Reset Everything

**Windows:**
```cmd
# Stop server
taskkill /IM python.exe

# Remove Bluetooth devices
# Settings → Devices → Bluetooth → Remove device

# Restart service
net stop BTHServ
net start BTHServ
```

**macOS:**
```bash
# Kill Python processes
killall python3

# Reset Bluetooth
sudo killall -9 bluetoothd

# Wait then restart Mac
```

**Linux:**
```bash
# Stop server
pkill -f server.py

# Reset Bluetooth
sudo systemctl restart bluetooth

# Clear pairing
rm -rf ~/.local/share/bluez/*
```

### Reinstall Application

```bash
# Remove old installation
rm -rf touchpad/

# Deep clean Python
pip cache purge

# Fresh clone
git clone https://github.com/yourusername/touchpad.git
cd touchpad

# Clean install
python -m venv venv_fresh
source venv_fresh/bin/activate
pip install -r server/requirements.txt

# Try again
python server/server.py --discover
```

---

If issues persist after trying these solutions, please open a GitHub issue with collected debug information.
