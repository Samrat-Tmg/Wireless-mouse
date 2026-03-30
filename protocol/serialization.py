"""
Binary serialization for Touchpad protocol messages.

Handles encoding and decoding of protocol messages to/from binary format.
Implements checksum validation and packet assembly.
"""

import struct
from typing import Tuple, Optional
from dataclasses import dataclass
from .constants import (
    PROTOCOL_MAGIC, PACKET_MIN_SIZE, MessageType, MAX_PACKET_SIZE
)


@dataclass
class CursorMove:
    """Cursor movement packet."""
    x: int
    y: int
    pressure: int = 255


@dataclass
class ScrollEvent:
    """Scroll wheel event."""
    delta_x: int
    delta_y: int


@dataclass
class GestureEvent:
    """Gesture command packet."""
    gesture_type: int
    intensity: int


class ProtocolSerializer:
    """Serializes and deserializes protocol messages."""

    @staticmethod
    def calculate_checksum(data: bytes) -> int:
        """Calculate XOR checksum for packet integrity."""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum & 0xFF

    @staticmethod
    def create_packet(message_type: int, payload: bytes = b'') -> bytes:
        """
        Create a complete protocol packet.
        
        Args:
            message_type: Type of message
            payload: Message payload
            
        Returns:
            Complete packet including header and checksum
        """
        if len(payload) > MAX_PACKET_SIZE - PACKET_MIN_SIZE:
            raise ValueError(f"Payload too large: {len(payload)}")

        header = bytes([PROTOCOL_MAGIC])
        msg_type = bytes([message_type])
        length = struct.pack('>H', len(payload))
        
        data = header + msg_type + length + payload
        checksum = bytes([ProtocolSerializer.calculate_checksum(data)])
        
        return data + checksum

    @staticmethod
    def parse_packet(data: bytes) -> Tuple[Optional[int], Optional[bytes]]:
        """
        Parse a protocol packet.
        
        Args:
            data: Raw packet bytes
            
        Returns:
            Tuple of (message_type, payload) or (None, None) if invalid
        """
        if len(data) < PACKET_MIN_SIZE:
            return None, None

        # Verify magic byte
        if data[0] != PROTOCOL_MAGIC:
            return None, None

        # Extract fields
        message_type = data[1]
        length = struct.unpack('>H', data[2:4])[0]
        payload = data[4:4+length]
        checksum = data[4+length]

        # Verify checksum
        expected_checksum = ProtocolSerializer.calculate_checksum(data[:-1])
        if checksum != expected_checksum:
            return None, None

        return message_type, payload

    @staticmethod
    def encode_cursor_move(x: int, y: int, pressure: int = 255) -> bytes:
        """Encode cursor move message."""
        return struct.pack('>HHB', x, y, pressure)

    @staticmethod
    def decode_cursor_move(payload: bytes) -> Optional[CursorMove]:
        """Decode cursor move message."""
        if len(payload) < 5:
            return None
        x, y, pressure = struct.unpack('>HHB', payload[:5])
        return CursorMove(x=x, y=y, pressure=pressure)

    @staticmethod
    def encode_scroll(delta_x: int, delta_y: int) -> bytes:
        """Encode scroll event."""
        return struct.pack('>hh', delta_x, delta_y)

    @staticmethod
    def decode_scroll(payload: bytes) -> Optional[ScrollEvent]:
        """Decode scroll event."""
        if len(payload) < 4:
            return None
        delta_x, delta_y = struct.unpack('>hh', payload[:4])
        return ScrollEvent(delta_x=delta_x, delta_y=delta_y)

    @staticmethod
    def encode_gesture(gesture_type: int, intensity: int) -> bytes:
        """Encode gesture command."""
        return struct.pack('>BB', gesture_type, intensity)

    @staticmethod
    def decode_gesture(payload: bytes) -> Optional[GestureEvent]:
        """Decode gesture command."""
        if len(payload) < 2:
            return None
        gesture_type, intensity = struct.unpack('>BB', payload[:2])
        return GestureEvent(gesture_type=gesture_type, intensity=intensity)

    @staticmethod
    def encode_ping() -> bytes:
        """Encode keep-alive ping."""
        import time
        timestamp = int(time.time() * 1000) & 0xFFFFFFFF
        return struct.pack('>I', timestamp)

    @staticmethod
    def encode_device_info(device_name: str, version: str) -> bytes:
        """Encode device information."""
        name_bytes = device_name.encode('utf-8')[:32]
        version_bytes = version.encode('utf-8')[:16]
        
        payload = struct.pack('B', len(name_bytes)) + name_bytes
        payload += struct.pack('B', len(version_bytes)) + version_bytes
        return payload
