"""Test suite for protocol serialization."""
import sys
sys.path.insert(0, '../')

import unittest
from protocol.serialization import ProtocolSerializer
from protocol.constants import MessageType


class TestProtocolSerializer(unittest.TestCase):
    """Test protocol serialization and deserialization."""

    def test_cursor_move_encoding(self):
        """Test cursor move message encoding."""
        payload = ProtocolSerializer.encode_cursor_move(100, 200, 255)
        self.assertEqual(len(payload), 5)

    def test_cursor_move_decoding(self):
        """Test cursor move message decoding."""
        payload = ProtocolSerializer.encode_cursor_move(100, 200, 255)
        move = ProtocolSerializer.decode_cursor_move(payload)
        self.assertIsNotNone(move)
        self.assertEqual(move.x, 100)
        self.assertEqual(move.y, 200)

    def test_scroll_encoding(self):
        """Test scroll message encoding."""
        payload = ProtocolSerializer.encode_scroll(5, -3)
        self.assertEqual(len(payload), 4)

    def test_scroll_decoding(self):
        """Test scroll message decoding."""
        payload = ProtocolSerializer.encode_scroll(5, -3)
        scroll = ProtocolSerializer.decode_scroll(payload)
        self.assertIsNotNone(scroll)
        self.assertEqual(scroll.delta_x, 5)
        self.assertEqual(scroll.delta_y, -3)

    def test_packet_creation(self):
        """Test packet creation with header and checksum."""
        packet = ProtocolSerializer.create_packet(MessageType.PING)
        self.assertGreaterEqual(len(packet), 5)

    def test_packet_parsing(self):
        """Test packet parsing."""
        original_packet = ProtocolSerializer.create_packet(MessageType.PING)
        msg_type, payload = ProtocolSerializer.parse_packet(original_packet)
        self.assertEqual(msg_type, MessageType.PING)

    def test_checksum_validation(self):
        """Test checksum validation."""
        packet = ProtocolSerializer.create_packet(MessageType.LEFT_CLICK)
        msg_type, _ = ProtocolSerializer.parse_packet(packet)
        self.assertIsNotNone(msg_type)

    def test_invalid_packet(self):
        """Test invalid packet handling."""
        invalid_packet = b'\xFF\xFF\xFF\xFF'
        msg_type, payload = ProtocolSerializer.parse_packet(invalid_packet)
        self.assertIsNone(msg_type)

    def test_device_info_encoding(self):
        """Test device info message encoding."""
        payload = ProtocolSerializer.encode_device_info("TestPC", "1.0.0")
        self.assertGreater(len(payload), 0)


class TestChecksum(unittest.TestCase):
    """Test checksum calculation."""

    def test_checksum_single_byte(self):
        """Test checksum for single byte."""
        data = b'\x01'
        checksum = ProtocolSerializer.calculate_checksum(data)
        self.assertEqual(checksum, 1)

    def test_checksum_multiple_bytes(self):
        """Test checksum for multiple bytes."""
        data = b'\x01\x02\x03'
        checksum = ProtocolSerializer.calculate_checksum(data)
        self.assertEqual(checksum, 0)  # 1 XOR 2 XOR 3 = 0

    def test_checksum_consistency(self):
        """Test checksum consistency."""
        data = b'Touchpad Protocol'
        checksum1 = ProtocolSerializer.calculate_checksum(data)
        checksum2 = ProtocolSerializer.calculate_checksum(data)
        self.assertEqual(checksum1, checksum2)


if __name__ == '__main__':
    unittest.main()
