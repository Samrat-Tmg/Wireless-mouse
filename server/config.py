"""
Configuration management for Touchpad server.

Handles loading and validating configuration from INI files
and environment variables.
"""

import configparser
import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration management."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file. If None, uses defaults.
        """
        self.config = configparser.ConfigParser()
        
        # Set defaults
        self._set_defaults()
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self.config.read(config_file)
            logger.info(f"Configuration loaded from {config_file}")

    def _set_defaults(self):
        """Set default configuration values."""
        self.config['bluetooth'] = {
            'adapter': 'hci0',
            'device_name': 'MyComputer-Touchpad',
            'service_uuid': '12345678-1234-5678-1234-567812345678',
            'port': '1',
        }
        
        self.config['input'] = {
            'mouse_speed': '1.5',
            'acceleration': 'true',
            'deadzone': '5',
            'invert_x': 'false',
            'invert_y': 'false',
        }
        
        self.config['network'] = {
            'listen_port': '5900',
            'max_connections': '5',
            'timeout': '30',
        }
        
        self.config['logging'] = {
            'level': 'INFO',
            'file': 'touchpad.log',
            'max_size': '10485760',  # 10MB
            'backup_count': '5',
        }

    def get_bluetooth_adapter(self) -> str:
        """Get Bluetooth adapter name."""
        return self.config.get('bluetooth', 'adapter', fallback='hci0')

    def get_device_name(self) -> str:
        """Get device name for discovery."""
        return self.config.get('bluetooth', 'device_name', 
                              fallback='MyComputer-Touchpad')

    def get_service_uuid(self) -> str:
        """Get Bluetooth service UUID."""
        return self.config.get('bluetooth', 'service_uuid',
                              fallback='12345678-1234-5678-1234-567812345678')

    def get_mouse_speed(self) -> float:
        """Get mouse movement speed multiplier."""
        try:
            speed = float(self.config.get('input', 'mouse_speed', fallback='1.5'))
            return max(0.1, min(5.0, speed))  # Clamp between 0.1 and 5.0
        except ValueError:
            return 1.5

    def get_acceleration_enabled(self) -> bool:
        """Check if cursor acceleration is enabled."""
        return self.config.getboolean('input', 'acceleration', fallback=True)

    def get_deadzone(self) -> int:
        """Get deadzone in pixels."""
        try:
            deadzone = int(self.config.get('input', 'deadzone', fallback='5'))
            return max(0, min(50, deadzone))  # Clamp between 0 and 50
        except ValueError:
            return 5

    def get_invert_x(self) -> bool:
        """Check if X axis is inverted."""
        return self.config.getboolean('input', 'invert_x', fallback=False)

    def get_invert_y(self) -> bool:
        """Check if Y axis is inverted."""
        return self.config.getboolean('input', 'invert_y', fallback=False)

    def get_listen_port(self) -> int:
        """Get TCP port for server."""
        try:
            port = int(self.config.get('network', 'listen_port', fallback='5900'))
            return max(1024, min(65535, port))  # Valid port range
        except ValueError:
            return 5900

    def get_max_connections(self) -> int:
        """Get maximum concurrent connections."""
        try:
            return int(self.config.get('network', 'max_connections', fallback='5'))
        except ValueError:
            return 5

    def get_connection_timeout(self) -> int:
        """Get connection timeout in seconds."""
        try:
            return int(self.config.get('network', 'timeout', fallback='30'))
        except ValueError:
            return 30

    def get_log_level(self) -> str:
        """Get logging level."""
        level = self.config.get('logging', 'level', fallback='INFO').upper()
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        return level if level in valid_levels else 'INFO'

    def get_log_file(self) -> str:
        """Get log file path."""
        return self.config.get('logging', 'file', fallback='touchpad.log')

    def get_log_max_size(self) -> int:
        """Get maximum log file size in bytes."""
        try:
            return int(self.config.get('logging', 'max_size', fallback='10485760'))
        except ValueError:
            return 10485760

    def get_log_backup_count(self) -> int:
        """Get number of log file backups to keep."""
        try:
            return int(self.config.get('logging', 'backup_count', fallback='5'))
        except ValueError:
            return 5

    def save(self, config_file: str) -> None:
        """Save configuration to file."""
        try:
            with open(config_file, 'w') as f:
                self.config.write(f)
            logger.info(f"Configuration saved to {config_file}")
        except IOError as e:
            logger.error(f"Failed to save configuration: {e}")

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        result = {}
        for section in self.config.sections():
            result[section] = dict(self.config.items(section))
        return result
