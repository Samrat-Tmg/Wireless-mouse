"""
Touchpad Wireless Mouse Server

Main server application for managing Bluetooth connections from mobile 
devices and translating touch input to system mouse control.
"""

import argparse
import logging
import sys
import signal
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from .config import Config
from .device_manager import create_device_manager, DeviceManager
from .input_controller import create_input_controller, InputController
from protocol import ProtocolSerializer, MessageType
import protocol.constants as proto_const


class TouchpadServer:
    """Main Touchpad server application."""

    def __init__(self, config_file: Optional[str] = None, debug: bool = False,
                 use_mock: bool = False):
        """
        Initialize Touchpad server.
        
        Args:
            config_file: Path to configuration file
            debug: Enable debug logging
            use_mock: Use mock device manager for testing
        """
        self.config = Config(config_file)
        self.device_manager: DeviceManager = create_device_manager(use_mock)
        self.input_controller: InputController = create_input_controller()
        self.debug = debug
        self.running = False
        
        self._setup_logging(debug)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("=" * 60)
        self.logger.info("Touchpad Wireless Mouse Server v1.0")
        self.logger.info("=" * 60)

    def _setup_logging(self, debug: bool = False) -> None:
        """
        Setup logging configuration.
        
        Args:
            debug: Enable debug level logging
        """
        log_level = logging.DEBUG if debug else logging.INFO
        log_level_str = self.config.get_log_level()
        
        if debug:
            log_level = logging.DEBUG
        else:
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL,
            }
            log_level = level_map.get(log_level_str, logging.INFO)

        # Create logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

        # File handler
        try:
            log_file = self.config.get_log_file()
            max_size = self.config.get_log_max_size()
            backup_count = self.config.get_log_backup_count()
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_size,
                backupCount=backup_count
            )
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
            
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
        except Exception as e:
            print(f"Failed to setup file logging: {e}")

    def _signal_handler(self, signum, frame):
        """Handle interrupt signal."""
        self.logger.info("Interrupt signal received")
        self.stop()

    def _process_packet(self, data: bytes) -> None:
        """
        Process incoming packet from mobile device.
        
        Args:
            data: Raw packet bytes
        """
        msg_type, payload = ProtocolSerializer.parse_packet(data)
        
        if msg_type is None:
            self.logger.warning("Invalid packet received")
            return

        try:
            if msg_type == MessageType.CURSOR_MOVE:
                cursor_move = ProtocolSerializer.decode_cursor_move(payload)
                if cursor_move:
                    # Apply sensitivity
                    speed = self.config.get_mouse_speed()
                    x = int(cursor_move.x * speed)
                    y = int(cursor_move.y * speed)
                    
                    # Apply inversion
                    if self.config.get_invert_x():
                        x = 1920 - x  # Assuming 1920x1080
                    if self.config.get_invert_y():
                        y = 1080 - y
                    
                    self.input_controller.move_mouse(x, y)
                    self.logger.debug(f"Cursor move: ({x}, {y})")

            elif msg_type == MessageType.LEFT_CLICK:
                self.input_controller.click_left()
                self.logger.debug("Left click")

            elif msg_type == MessageType.RIGHT_CLICK:
                self.input_controller.click_right()
                self.logger.debug("Right click")

            elif msg_type == MessageType.MIDDLE_CLICK:
                self.input_controller.click_middle()
                self.logger.debug("Middle click")

            elif msg_type == MessageType.SCROLL:
                scroll = ProtocolSerializer.decode_scroll(payload)
                if scroll:
                    self.input_controller.scroll(scroll.delta_x, scroll.delta_y)
                    self.logger.debug(f"Scroll: ({scroll.delta_x}, {scroll.delta_y})")

            elif msg_type == MessageType.PING:
                self.logger.debug("Ping received")
                # Send pong response
                pong_packet = ProtocolSerializer.create_packet(MessageType.PONG)
                # Response would be sent back to device

            elif msg_type == MessageType.GESTURE:
                gesture = ProtocolSerializer.decode_gesture(payload)
                if gesture:
                    self.logger.debug(f"Gesture: type={gesture.gesture_type}, "
                                    f"intensity={gesture.intensity}")

            else:
                self.logger.warning(f"Unknown message type: {msg_type}")

        except Exception as e:
            self.logger.error(f"Error processing packet: {e}")

    def _on_data_received(self, device_address: str, data: bytes) -> None:
        """
        Callback for incoming data from device.
        
        Args:
            device_address: Bluetooth address of device
            data: Received data
        """
        self.logger.debug(f"Data from {device_address}: {len(data)} bytes")
        self._process_packet(data)

    def start(self) -> None:
        """Start the server."""
        self.running = True
        self.logger.info("Starting Touchpad server...")

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # Start listening for connections
            self.device_manager.start_listening(self._on_data_received)
            
            self.logger.info("Server started successfully")
            self.logger.info(f"Device name: {self.config.get_device_name()}")
            self.logger.info("Waiting for mobile connections...")

            # Keep server running
            while self.running:
                time.sleep(1)

        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the server."""
        self.logger.info("Stopping server...")
        self.running = False
        
        try:
            self.device_manager.stop_listening()
            self.logger.info("Server stopped")
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")

    def discover_devices(self, timeout: int = 10) -> None:
        """
        Discover available Bluetooth devices.
        
        Args:
            timeout: Discovery timeout in seconds
        """
        self.logger.info(f"Discovering devices (timeout={timeout}s)...")
        devices = self.device_manager.discover_devices(timeout)
        
        if not devices:
            self.logger.info("No devices found")
            return

        self.logger.info(f"Found {len(devices)} device(s):")
        for device in devices:
            status = "paired" if device.paired else "unpaired"
            self.logger.info(f"  - {device.name} ({device.address}) [{status}]")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Touchpad Wireless Mouse Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python server.py                    # Start server with defaults
  python server.py --debug            # Start with debug logging
  python server.py --config custom.ini  # Use custom config
  python server.py --discover         # Discover devices
  python server.py --mock             # Use mock device manager
        '''
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--discover',
        action='store_true',
        help='Discover available devices'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock device manager for testing'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Device discovery timeout in seconds'
    )

    args = parser.parse_args()

    try:
        server = TouchpadServer(
            config_file=args.config,
            debug=args.debug,
            use_mock=args.mock
        )

        if args.discover:
            server.discover_devices(timeout=args.timeout)
        else:
            server.start()

    except KeyboardInterrupt:
        print("\nShutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
