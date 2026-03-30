"""
Protocol constants and definitions for Touchpad wireless mouse.

This module defines the communication protocol between mobile client
and desktop server, including message types, packet structure, and
protocol version information.
"""

# Protocol version
PROTOCOL_VERSION = 1
PROTOCOL_MAGIC = 0xAD

# Packet structure constants
PACKET_HEADER_SIZE = 1  # Magic byte
PACKET_TYPE_SIZE = 1
PACKET_LENGTH_SIZE = 2
PACKET_CHECKSUM_SIZE = 1
PACKET_MIN_SIZE = PACKET_HEADER_SIZE + PACKET_TYPE_SIZE + PACKET_LENGTH_SIZE + PACKET_CHECKSUM_SIZE

# Message types
class MessageType:
    """Message type constants."""
    CURSOR_MOVE = 0x01
    LEFT_CLICK = 0x02
    RIGHT_CLICK = 0x03
    SCROLL = 0x04
    GESTURE = 0x05
    PING = 0x06
    PONG = 0x07
    MOUSE_RELEASE = 0x08
    MIDDLE_CLICK = 0x09
    DOUBLE_CLICK = 0x0A
    SENSITIVITY_UPDATE = 0x0B
    DEVICE_INFO = 0x0C
    ERROR = 0xFF

# Gesture types
class GestureType:
    """Gesture command types."""
    SWIPE_LEFT = 0x01
    SWIPE_RIGHT = 0x02
    SWIPE_UP = 0x03
    SWIPE_DOWN = 0x04
    PINCH_IN = 0x05
    PINCH_OUT = 0x06
    TWO_FINGER_TAP = 0x07
    THREE_FINGER_TAP = 0x08

# Bluetooth service and characteristics UUIDs
SERVICE_UUID = "0000180A-0000-1000-8000-00805F9B34FB"
CHARACTERISTICS_UUID = "00002A37-0000-1000-8000-00805F9B34FB"

# Device discovery parameters
DISCOVERY_TIMEOUT = 10
DISCOVERY_RETRY_COUNT = 3

# Connection parameters
CONNECTION_TIMEOUT = 30
KEEP_ALIVE_INTERVAL = 5  # seconds
MAX_PACKET_SIZE = 1024

# Input sensitivity
MIN_SENSITIVITY = 0.5
MAX_SENSITIVITY = 3.0
DEFAULT_SENSITIVITY = 1.5

# Coordinate ranges (virtual screen)
MAX_X_COORD = 1920
MAX_Y_COORD = 1080

# Acceleration parameters
ACCELERATION_THRESHOLD = 10  # pixels/update
ACCELERATION_MULTIPLIER = 1.2
