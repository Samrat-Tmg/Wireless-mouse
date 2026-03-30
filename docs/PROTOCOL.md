# Protocol Specification

## Protocol Overview

Touchpad uses a custom binary protocol for communication between mobile client and desktop server over Bluetooth RFCOMM.

**Protocol Version**: 1.0  
**Transport**: Bluetooth RFCOMM (Serial Port Profile)  
**Data Format**: Binary big-endian

## Packet Format

### General Packet Structure

```
[Magic] [Type] [Length] [Payload] [Checksum]
[1 byte][1 byte][2 bytes][n bytes][1 byte]
```

| Field | Size | Description |
|-------|------|-------------|
| Magic | 1 byte | Protocol identifier (0xAD) |
| Type | 1 byte | Message type identifier |
| Length | 2 bytes | Length of payload (big-endian) |
| Payload | 0-1022 bytes | Message-specific data |
| Checksum | 1 byte | XOR checksum of all fields before checksum |

### Maximum Packet Size

1024 bytes total (1 + 1 + 2 + 1020 + 1 overhead for 1022 payload bytes)

## Message Types

### 0x01: CURSOR_MOVE

Move the mouse cursor to absolute coordinates.

**Payload Structure:**
```
[X coord] [Y coord] [Pressure]
[2 bytes] [2 bytes] [1 byte]
```

| Field | Size | Range | Description |
|-------|------|-------|-------------|
| X | 2 bytes | 0-1920 | X coordinate (normalized to 0-1920) |
| Y | 2 bytes | 0-1080 | Y coordinate (normalized to 0-1080) |
| Pressure | 1 byte | 0-255 | Touch pressure (255 = max pressure) |

**Example:**
```
AD 01 00 05 00 64 00 C8 FF 2D
AD = Magic
01 = CURSOR_MOVE
00 05 = Length (5 bytes)
00 64 = X = 100
00 C8 = Y = 200
FF = Pressure = 255
2D = Checksum
```

**Frequency**: 30-60 Hz during active touch

### 0x02: LEFT_CLICK

Simulate left mouse button click.

**Payload Structure:**
```
(empty)
```

**Example:**
```
AD 02 00 00 AF
AD = Magic
02 = LEFT_CLICK
00 00 = Length (0 bytes)
AF = Checksum
```

### 0x03: RIGHT_CLICK

Simulate right mouse button click.

**Payload Structure:**
```
(empty)
```

### 0x04: SCROLL

Simulate mouse wheel scroll.

**Payload Structure:**
```
[Delta X] [Delta Y]
[2 bytes] [2 bytes]
```

| Field | Size | Description |
|-------|------|-------------|
| Delta X | 2 bytes (signed) | Horizontal scroll amount |
| Delta Y | 2 bytes (signed) | Vertical scroll amount (negative = up) |

**Example (scroll down 3 clicks):**
```
AD 04 00 04 00 00 FF FD 05
AD = Magic
04 = SCROLL
00 04 = Length (4 bytes)
00 00 = Delta X = 0
FF FD = Delta Y = -3
05 = Checksum
```

### 0x05: GESTURE

Send multi-touch gesture command.

**Payload Structure:**
```
[Gesture Type] [Intensity]
[1 byte]       [1 byte]
```

**Gesture Types:**
- 0x01: SWIPE_LEFT
- 0x02: SWIPE_RIGHT
- 0x03: SWIPE_UP
- 0x04: SWIPE_DOWN
- 0x05: PINCH_IN
- 0x06: PINCH_OUT
- 0x07: TWO_FINGER_TAP
- 0x08: THREE_FINGER_TAP

| Field | Size | Range | Description |
|-------|------|-------|-------------|
| Gesture Type | 1 byte | 0x01-0x08 | Gesture identifier |
| Intensity | 1 byte | 0-255 | Gesture intensity/velocity |

### 0x06: PING

Keep-alive heartbeat from client.

**Payload Structure:**
```
[Timestamp]
[4 bytes]
```

| Field | Size | Description |
|-------|------|-------------|
| Timestamp | 4 bytes | Milliseconds since epoch (32-bit) |

**Frequency**: Every 5 seconds

### 0x07: PONG

Keep-alive response from server.

**Payload Structure:**
```
[Timestamp Echo]
[4 bytes]
```

### 0x08: MOUSE_RELEASE

Release all pressed mouse buttons.

**Payload Structure:**
```
(empty)
```

### 0x09: MIDDLE_CLICK

Simulate middle mouse button click.

**Payload Structure:**
```
(empty)
```

### 0x0A: DOUBLE_CLICK

Simulate double-click.

**Payload Structure:**
```
(empty)
```

### 0x0B: SENSITIVITY_UPDATE

Update cursor sensitivity on the fly.

**Payload Structure:**
```
[Sensitivity]
[1 byte]
```

| Field | Size | Range | Description |
|-------|------|-------|-------------|
| Sensitivity | 1 byte | 50-250 | Sensitivity percentage (100 = 1.0x) |

### 0x0C: DEVICE_INFO

Exchange device information.

**Payload Structure:**
```
[Name Length] [Name] [Version Length] [Version]
[1 byte]      [n]    [1 byte]         [m]
```

### 0xFF: ERROR

Error notification.

**Payload Structure:**
```
[Error Code] [Message Length] [Message]
[1 byte]     [1 byte]         [n]
```

**Error Codes:**
- 0x01: Unknown message type
- 0x02: Checksum invalid
- 0x03: Payload too large
- 0x04: Protocol version mismatch
- 0x05: Device not ready

## Checksum Algorithm

XOR of all bytes in the packet before the checksum field:

```python
checksum = 0
for byte in (magic + type + length + payload):
    checksum ^= byte
checksum &= 0xFF
```

## Coordinate System

Coordinates are normalized to virtual screen size (0-1920 x 0-1080) regardless of actual device resolution.

Desktop server maps these to actual display resolution:

```
desktop_x = (normalized_x / 1920) * display_width
desktop_y = (normalized_y / 1080) * display_height
```

## Connection Workflow

```
1. Client initiates Bluetooth RFCOMM connection to server
2. Server accepts and sends DEVICE_INFO message
3. Client responds with DEVICE_INFO
4. Periodic PING/PONG messages exchanged every 5 seconds
5. Client sends input events (CURSOR_MOVE, CLICK, etc.)
6. Server responds with input simulation
7. On disconnect: close RFCOMM socket
```

## Error Handling

- **Invalid Checksum**: Server discards packet and optionally sends ERROR message
- **Unknown Message Type**: Server sends ERROR (0xFF) message
- **Oversized Payload**: Server rejects and sends ERROR message
- **Connection Loss**: Both sides close connections gracefully

## Performance Considerations

- **Packet Overhead**: 5 bytes minimum, 7 bytes with data
- **Maximum Throughput**: 60 packets/second (typical)
- **Latency Budget**: 50-150ms for full round-trip
- **Bandwidth**: ~300 bytes/second typical movement data

## Version Compatibility

Current protocol version is 1.0. Clients and servers must match major version numbers.

Future versions will include:
- Version 1.1: Keyboard support
- Version 2.0: Multi-device support
- Version 3.0: Custom gesture definitions

## Example Message Sequences

### Pointer Movement

```
Client --> Server: CURSOR_MOVE (600, 400, 200)
Client --> Server: CURSOR_MOVE (610, 405, 210)
Client --> Server: CURSOR_MOVE (620, 410, 220)
... (30-60 Hz update rate)
```

### Click Action

```
Client --> Server: CURSOR_MOVE (500, 500, 255)
Client --> Server: LEFT_CLICK
Client --> Server: CURSOR_MOVE (505, 505, 100)
```

### Scroll Action

```
Client --> Server: SCROLL (0, -5)      # Scroll up 5 clicks
Client --> Server: SCROLL (0, 5)       # Scroll down 5 clicks
```

### Keep-Alive

```
Client --> Server: PING (1234567890)
Server --> Client: PONG (1234567890)
... (every 5 seconds)
```
