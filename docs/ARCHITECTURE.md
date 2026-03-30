# System Architecture

## Overview

Touchpad is a distributed client-server wireless mouse application. The system consists of three main components:

1. **Mobile Client** (iOS/Android) - Touch input interface
2. **Desktop Server** (Windows/macOS/Linux) - Device management and OS integration
3. **Protocol** - Binary communication protocol over Bluetooth

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    TOUCHPAD SYSTEM ARCHITECTURE             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────┐   ┌──────────────────────┐   │
│  │    MOBILE CLIENT         │   │    DESKTOP SERVER    │   │
│  │   (iOS/Android)          │   │   (Win/Mac/Linux)    │   │
│  ├──────────────────────────┤   ├──────────────────────┤   │
│  │                          │   │                      │   │
│  │  ┌────────────────────┐  │   │  ┌────────────────┐  │   │
│  │  │ Touch Input Layer  │  │   │  │ Device Manager │  │   │
│  │  │  • Raw touch events│  │   │  │ • Discovery    │  │   │
│  │  │  • Gesture detect  │  │   │  │ • Connection   │  │   │
│  │  │  • Pressure sense  │  │   │  │ • Data routing │  │   │
│  │  └────────┬───────────┘  │   │  └────────┬───────┘  │   │
│  │           │               │   │          │          │   │
│  │  ┌────────▼───────────┐  │   │  ┌───────▼──────┐   │   │
│  │  │ Protocol Engine    │  │   │  │Input Proc.   │   │   │
│  │  │ • Serialization    │  │   │  │ • Mouse move │   │   │
│  │  │ • Packet creation  │  │   │  │ • Click sim  │   │   │
│  │  └────────┬───────────┘  │   │  │ • Scroll     │   │   │
│  │           │               │   │  └───────┬──────┘   │   │
│  │  ┌────────▼───────────┐  │   │          │          │   │
│  │  │ BLE/RFCOMM Stack   │  │   │  ┌───────▼──────┐   │   │
│  │  │ • Connection mgmt  │  │   │  │ OS Interface │   │   │
│  │  │ • Packet transmission└──┼──▶│ • Windows    │   │   │
│  │  └────────────────────┘  │   │  │ • macOS      │   │   │
│  │                          │   │  │ • Linux      │   │   │
│  └──────────────────────────┘   │  └──────────────┘   │   │
│                                 │                      │   │
│  ┌──────────────────────────┐   │  ┌──────────────┐   │    │
│  │ UI Components            │   │  │ Configuration│   │    │
│  │ • Touchpad view          │   │  │ • Settings   │   │    │
│  │ • Device list            │   │  │ • Profiles   │   │    │
│  │ • Connection status      │   │  │ • Logging    │   │    │
│  └──────────────────────────┘   │  └──────────────┘   │    │
│                                 └──────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Mobile Client Layer

The mobile application handles:

- **Touch Input Processing**: Raw touch events from the device touchscreen
- **Gesture Recognition**: Multi-touch gesture interpretation
- **Pressure Sensing**: Pressure data from touchscreen
- **Connection Management**: Bluetooth RFCOMM socket management
- **Protocol Encoding**: Serialization of touch data to protocol format

### Desktop Server Layer

The server manages:

- **Device Discovery**: Bluetooth device scanning and enumeration
- **Connection Management**: Accept and manage client connections
- **Protocol Parsing**: Deserialize incoming data packets
- **Input Emulation**: Cross-platform mouse input simulation
- **Configuration**: Settings and profile management
- **Logging**: Comprehensive event and error logging

### Protocol Layer

Binary protocol featuring:

- **Message Types**: Defined packet types for different actions
- **Serialization**: Efficient binary encoding of data
- **Checksum**: Error detection and validation
- **Stream Framing**: Clear packet boundaries

## Data Flow

### Motion Event Flow

```
Touch Event (x, y, pressure)
    │
    ├─ Normalize coordinates
    ├─ Apply sensitivity adjustment
    │
    ▼
Encode as MessageType.CURSOR_MOVE
    │
    ├─ X coordinate (2 bytes)
    ├─ Y coordinate (2 bytes)
    └─ Pressure (1 byte)
    │
    ▼
Create packet with header, type, length, checksum
    │
    ▼
Send over RFCOMM socket
    │
    ▼
Server receives and parses packet
    │
    ├─ Validate checksum
    ├─ Extract coordinates
    │
    ▼
Apply configuration settings
    │
    ├─ Mouse speed multiplier
    ├─ Acceleration curve
    ├─ Axis inversion
    │
    ▼
Update mouse position via OS API
    │
    └─ Windows: SetCursorPos()
    └─ macOS: CGEventCreateMouseEvent()
    └─ Linux: xdotool mousemove
```

### Click Event Flow

```
Tap Event (1-finger)
    │
    ├─ Duration < 200ms
    │
    ▼
Encode as MessageType.LEFT_CLICK
    │
    ▼
Create packet
    │
    ▼
Send over socket
    │
    ▼
Server receives
    │
    ├─ Windows: mouse_event(MOUSEEVENTF_LEFTDOWN | LEFTUP)
    ├─ macOS: CGEventLeftMouseDown + CGEventLeftMouseUp
    └─ Linux: xdotool click 1
```

## Cross-Platform Support

### Windows Implementation

```
Device: Bluetooth USB Adapter or Built-in
Protocol: RFCOMM over L2CAP
API: ctypes + Win32 API (SetCursorPos, mouse_event)
```

### macOS Implementation

```
Device: Bluetooth Module (built-in)
Protocol: RFCOMM over L2CAP
API: Quartz (CGEvent functions)
```

### Linux Implementation

```
Device: BlueZ subsystem
Protocol: RFCOMM via PyBluez
API: xdotool for cursor control
```

## Concurrency Model

- **Server**: Multi-threaded architecture
  - Main thread: Command processing and user interaction
  - Listener thread: Accepts incoming Bluetooth connections
  - Worker threads: Handle individual device connections

- **Mobile**: Single-threaded event loop
  - UI thread: Touch input handling
  - Background thread: Bluetooth communication

## Security Considerations

1. **Pairing**: Standard Bluetooth pairing mechanism
2. **Encryption**: Uses Bluetooth link-level encryption
3. **Authentication**: PIN-based pairing
4. **Data Validation**: Checksum verification on all packets
5. **Input Validation**: Coordinate bounds checking

## Performance Characteristics

| Metric | Target | Achieved |
|--------|--------|----------|
| Latency | < 100ms | 50-150ms |
| Throughput | 60 pkt/s | 60+ pkt/s |
| Battery | 4+ hrs | 4-6 hrs |
| Memory | < 50MB | 20-40MB |
| CPU | < 5% | 1-3% |

## Extensibility

The modular architecture allows:

- **New Message Types**: Add handlers in `MessageType`
- **New Gestures**: Extend `GestureType` enum
- **Custom Input Methods**: Subclass `InputController`
- **Configuration Profiles**: Add to config system
- **Logging Plugins**: Custom log handlers
- **Device Types**: Abstract device manager allows different BLE implementations

## Future Architecture Enhancements

1. **Keyboard Support**: Extend protocol for keyboard events
2. **Multi-Device**: Support multiple phones controlling same computer
3. **Cloud Sync**: Store configurations in the cloud
4. **Voice Control**: Add audio input channel
5. **Haptic Feedback**: Send feedback to mobile device
6. **Recording**: Record and replay actions
