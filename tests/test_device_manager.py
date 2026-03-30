"""Test suite for device manager."""
import sys
sys.path.insert(0, '../server')

import unittest
from device_manager import MockDeviceManager


class TestDeviceManager(unittest.TestCase):
    """Test device manager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = MockDeviceManager()

    def test_device_discovery(self):
        """Test device discovery."""
        devices = self.manager.discover_devices(timeout=1)
        self.assertIsInstance(devices, list)
        # Mock should return at least one device
        self.assertGreater(len(devices), 0)

    def test_connect_device(self):
        """Test device connection."""
        devices = self.manager.discover_devices(timeout=1)
        if devices:
            device = devices[0]
            result = self.manager.connect(device.address)
            self.assertTrue(result)

    def test_disconnect_device(self):
        """Test device disconnection."""
        devices = self.manager.discover_devices(timeout=1)
        if devices:
            device = devices[0]
            self.manager.connect(device.address)
            result = self.manager.disconnect(device.address)
            self.assertTrue(result)

    def test_get_connected_devices(self):
        """Test getting connected devices."""
        devices = self.manager.discover_devices(timeout=1)
        if devices:
            device = devices[0]
            self.manager.connect(device.address)
            connected = self.manager.get_connected_devices()
            self.assertEqual(len(connected), 1)

    def test_listening(self):
        """Test listening for connections."""
        def callback(addr, data):
            pass

        self.manager.start_listening(callback)
        self.assertTrue(self.manager.listening)
        
        self.manager.stop_listening()
        self.assertFalse(self.manager.listening)


if __name__ == '__main__':
    unittest.main()
