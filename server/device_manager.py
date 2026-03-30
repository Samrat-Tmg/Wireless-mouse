"""
Bluetooth device manager for Touchpad server.

Handles device discovery, pairing, and connection management
over Bluetooth.
"""

import logging
import socket
import sys
import threading
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class BluetoothDevice:
    """Bluetooth device information."""
    address: str
    name: str
    rssi: int
    paired: bool = False
    connected: bool = False


class DeviceManager(ABC):
    """Abstract base class for Bluetooth device management."""

    @abstractmethod
    def discover_devices(self, timeout: int = 10) -> List[BluetoothDevice]:
        """Discover available Bluetooth devices."""
        pass

    @abstractmethod
    def connect(self, device_address: str) -> bool:
        """Connect to a device."""
        pass

    @abstractmethod
    def disconnect(self, device_address: str) -> bool:
        """Disconnect from device."""
        pass

    @abstractmethod
    def get_connected_devices(self) -> List[BluetoothDevice]:
        """Get list of connected devices."""
        pass

    @abstractmethod
    def send_data(self, device_address: str, data: bytes) -> bool:
        """Send data to device."""
        pass

    @abstractmethod
    def receive_data(self, device_address: str, 
                    timeout: int = 5) -> Optional[bytes]:
        """Receive data from device."""
        pass

    @abstractmethod
    def start_listening(self, callback: Callable[[str, bytes], None]) -> None:
        """Start listening for incoming connections."""
        pass

    @abstractmethod
    def stop_listening(self) -> None:
        """Stop listening for incoming connections."""
        pass


class MockDeviceManager(DeviceManager):
    """Mock device manager for testing without Bluetooth hardware."""

    def __init__(self):
        """Initialize mock device manager."""
        self.devices: Dict[str, BluetoothDevice] = {}
        self.connected_devices: Dict[str, socket.socket] = {}
        self.listening = False
        self.callback: Optional[Callable] = None
        logger.info("Mock Bluetooth device manager initialized")

    def discover_devices(self, timeout: int = 10) -> List[BluetoothDevice]:
        """Discover devices (mock implementation)."""
        logger.info(f"Mock: Discovering devices for {timeout}s")
        # Return mock device
        mock_device = BluetoothDevice(
            address="00:11:22:33:44:55",
            name="iPhone-Touchpad",
            rssi=-45,
            paired=True,
            connected=False
        )
        self.devices["00:11:22:33:44:55"] = mock_device
        return [mock_device]

    def connect(self, device_address: str) -> bool:
        """Connect to device (mock)."""
        logger.info(f"Mock: Connecting to {device_address}")
        if device_address in self.devices:
            self.devices[device_address].connected = True
            self.connected_devices[device_address] = None  # Mock socket
            return True
        return False

    def disconnect(self, device_address: str) -> bool:
        """Disconnect from device (mock)."""
        logger.info(f"Mock: Disconnecting from {device_address}")
        if device_address in self.connected_devices:
            self.devices[device_address].connected = False
            del self.connected_devices[device_address]
            return True
        return False

    def get_connected_devices(self) -> List[BluetoothDevice]:
        """Get connected devices."""
        return [d for d in self.devices.values() if d.connected]

    def send_data(self, device_address: str, data: bytes) -> bool:
        """Send data (mock)."""
        return device_address in self.connected_devices

    def receive_data(self, device_address: str,
                    timeout: int = 5) -> Optional[bytes]:
        """Receive data (mock)."""
        return None

    def start_listening(self, callback: Callable[[str, bytes], None]) -> None:
        """Start listening (mock)."""
        self.callback = callback
        self.listening = True
        logger.info("Mock: Started listening for connections")

    def stop_listening(self) -> None:
        """Stop listening (mock)."""
        self.listening = False
        logger.info("Mock: Stopped listening")


class BluetoothDeviceManager(DeviceManager):
    """Bluetooth device manager using PyBluez."""

    def __init__(self):
        """Initialize Bluetooth device manager."""
        try:
            import bluetooth
            self.bluetooth = bluetooth
            self.devices: Dict[str, BluetoothDevice] = {}
            self.connected_devices: Dict[str, socket.socket] = {}
            self.listening = False
            self.listen_thread: Optional[threading.Thread] = None
            self.callback: Optional[Callable] = None
            logger.info("Bluetooth device manager initialized")
        except ImportError:
            logger.warning("PyBluez not available, using mock manager")
            self.bluetooth = None

    def discover_devices(self, timeout: int = 10) -> List[BluetoothDevice]:
        """Discover available Bluetooth devices."""
        if not self.bluetooth:
            logger.warning("Bluetooth not available")
            return []

        try:
            logger.info(f"Scanning for devices (timeout={timeout}s)")
            nearby_devices = self.bluetooth.discover_devices(
                duration=timeout,
                lookup_names=True,
                flush_cache=True
            )

            devices = []
            for address, name in nearby_devices:
                device = BluetoothDevice(
                    address=address,
                    name=name,
                    rssi=0,  # RSSI not available via discover_devices
                    paired=self._is_paired(address)
                )
                self.devices[address] = device
                devices.append(device)
                logger.debug(f"Found device: {name} ({address})")

            logger.info(f"Discovery complete: {len(devices)} devices found")
            return devices
        except Exception as e:
            logger.error(f"Device discovery failed: {e}")
            return []

    def connect(self, device_address: str) -> bool:
        """Connect to a device."""
        if not self.bluetooth:
            logger.warning("Bluetooth not available")
            return False

        try:
            logger.info(f"Connecting to {device_address}")
            sock = self.bluetooth.BluetoothSocket(self.bluetooth.RFCOMM)
            sock.connect((device_address, 1))
            
            self.connected_devices[device_address] = sock
            if device_address in self.devices:
                self.devices[device_address].connected = True
            
            logger.info(f"Successfully connected to {device_address}")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def disconnect(self, device_address: str) -> bool:
        """Disconnect from device."""
        try:
            if device_address in self.connected_devices:
                sock = self.connected_devices[device_address]
                sock.close()
                del self.connected_devices[device_address]
                
                if device_address in self.devices:
                    self.devices[device_address].connected = False
                
                logger.info(f"Disconnected from {device_address}")
                return True
        except Exception as e:
            logger.error(f"Disconnection failed: {e}")
        return False

    def get_connected_devices(self) -> List[BluetoothDevice]:
        """Get connected devices."""
        return [d for d in self.devices.values() if d.connected]

    def send_data(self, device_address: str, data: bytes) -> bool:
        """Send data to device."""
        try:
            if device_address not in self.connected_devices:
                logger.warning(f"Device {device_address} not connected")
                return False

            sock = self.connected_devices[device_address]
            sock.sendall(data)
            return True
        except Exception as e:
            logger.error(f"Failed to send data: {e}")
            return False

    def receive_data(self, device_address: str,
                    timeout: int = 5) -> Optional[bytes]:
        """Receive data from device."""
        try:
            if device_address not in self.connected_devices:
                return None

            sock = self.connected_devices[device_address]
            sock.settimeout(timeout)
            data = sock.recv(1024)
            return data if data else None
        except socket.timeout:
            return None
        except Exception as e:
            logger.error(f"Failed to receive data: {e}")
            return None

    def _is_paired(self, device_address: str) -> bool:
        """Check if device is already paired."""
        # Implementation depends on OS
        return False

    def start_listening(self, callback: Callable[[str, bytes], None]) -> None:
        """Start listening for incoming connections."""
        if not self.bluetooth:
            logger.warning("Bluetooth not available")
            return

        self.callback = callback
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen, daemon=True)
        self.listen_thread.start()
        logger.info("Started listening for Bluetooth connections")

    def stop_listening(self) -> None:
        """Stop listening for incoming connections."""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=5)
        logger.info("Stopped listening for Bluetooth connections")

    def _listen(self) -> None:
        """Listen thread for incoming connections."""
        try:
            server_sock = self.bluetooth.BluetoothSocket(self.bluetooth.RFCOMM)
            server_sock.bind(("", self.bluetooth.PORT_ANY))
            server_sock.listen(1)

            port = server_sock.getsockname()[1]
            logger.info(f"Listening on RFCOMM port {port}")

            while self.listening:
                try:
                    client_sock, client_addr = server_sock.accept()
                    logger.info(f"Connection from {client_addr}")

                    if self.callback:
                        data = client_sock.recv(1024)
                        self.callback(client_addr, data)

                    client_sock.close()
                except socket.timeout:
                    continue

            server_sock.close()
        except Exception as e:
            logger.error(f"Listen thread error: {e}")


def create_device_manager(use_mock: bool = False) -> DeviceManager:
    """
    Factory function to create device manager.
    
    Args:
        use_mock: If True, use mock manager for testing
        
    Returns:
        DeviceManager instance
    """
    if use_mock:
        return MockDeviceManager()
    
    try:
        return BluetoothDeviceManager()
    except ImportError:
        logger.warning("PyBluez not available, falling back to mock manager")
        return MockDeviceManager()
