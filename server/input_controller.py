"""
Operating system level input control.

Provides cross-platform mouse and keyboard input control for
Windows, macOS, and Linux systems.
"""

import sys
import logging
from typing import Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MousePosition:
    """Mouse position data."""
    x: int
    y: int


class InputController(ABC):
    """Abstract base class for input control."""

    @abstractmethod
    def move_mouse(self, x: int, y: int) -> None:
        """Move mouse cursor."""
        pass

    @abstractmethod
    def click_left(self) -> None:
        """Simulate left click."""
        pass

    @abstractmethod
    def click_right(self) -> None:
        """Simulate right click."""
        pass

    @abstractmethod
    def click_middle(self) -> None:
        """Simulate middle click."""
        pass

    @abstractmethod
    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Simulate scroll wheel."""
        pass

    @abstractmethod
    def get_mouse_position(self) -> MousePosition:
        """Get current mouse position."""
        pass

    @abstractmethod
    def release_all_buttons(self) -> None:
        """Release all pressed mouse buttons."""
        pass


class WindowsInputController(InputController):
    """Input controller for Windows systems."""

    def __init__(self):
        """Initialize Windows input controller."""
        try:
            import ctypes
            self.ctypes = ctypes
            logger.info("Windows input controller initialized")
        except ImportError:
            logger.error("Failed to import ctypes for Windows")

    def move_mouse(self, x: int, y: int) -> None:
        """Move mouse to absolute position."""
        try:
            self.ctypes.windll.user32.SetCursorPos(int(x), int(y))
        except Exception as e:
            logger.error(f"Failed to move mouse: {e}")

    def click_left(self) -> None:
        """Left mouse click."""
        try:
            self.ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
            self.ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
        except Exception as e:
            logger.error(f"Failed to click left: {e}")

    def click_right(self) -> None:
        """Right mouse click."""
        try:
            self.ctypes.windll.user32.mouse_event(8, 0, 0, 0, 0)   # MOUSEEVENTF_RIGHTDOWN
            self.ctypes.windll.user32.mouse_event(16, 0, 0, 0, 0)  # MOUSEEVENTF_RIGHTUP
        except Exception as e:
            logger.error(f"Failed to click right: {e}")

    def click_middle(self) -> None:
        """Middle mouse click."""
        try:
            self.ctypes.windll.user32.mouse_event(32, 0, 0, 0, 0)  # MOUSEEVENTF_MIDDLEDOWN
            self.ctypes.windll.user32.mouse_event(64, 0, 0, 0, 0)  # MOUSEEVENTF_MIDDLEUP
        except Exception as e:
            logger.error(f"Failed to click middle: {e}")

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Scroll wheel."""
        try:
            if delta_y != 0:
                self.ctypes.windll.user32.mouse_event(2048, 0, 0, delta_y * 120, 0)
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")

    def get_mouse_position(self) -> MousePosition:
        """Get current mouse position."""
        try:
            x = self.ctypes.wintypes.LONG()
            y = self.ctypes.wintypes.LONG()
            self.ctypes.windll.user32.GetCursorPos(self.ctypes.byref(x), self.ctypes.byref(y))
            return MousePosition(x=x.value, y=y.value)
        except Exception as e:
            logger.error(f"Failed to get mouse position: {e}")
            return MousePosition(x=0, y=0)

    def release_all_buttons(self) -> None:
        """Release all mouse buttons."""
        pass


class MacOSInputController(InputController):
    """Input controller for macOS systems."""

    def __init__(self):
        """Initialize macOS input controller."""
        try:
            from Quartz import CGEventCreateMouseEvent, CGEventPost
            from Quartz import kCGHIDEventTap
            from Quartz import CGEventLeftMouseDown, CGEventLeftMouseUp
            from Quartz import CGEventRightMouseDown, CGEventRightMouseUp
            from Quartz import CGEventOtherMouseDown, CGEventOtherMouseUp
            from Quartz import CGEventScrollWheel
            
            self.CGEventCreateMouseEvent = CGEventCreateMouseEvent
            self.CGEventPost = CGEventPost
            self.kCGHIDEventTap = kCGHIDEventTap
            self.CGEventLeftMouseDown = CGEventLeftMouseDown
            self.CGEventLeftMouseUp = CGEventLeftMouseUp
            self.CGEventRightMouseDown = CGEventRightMouseDown
            self.CGEventRightMouseUp = CGEventRightMouseUp
            self.CGEventOtherMouseDown = CGEventOtherMouseDown
            self.CGEventOtherMouseUp = CGEventOtherMouseUp
            self.CGEventScrollWheel = CGEventScrollWheel
            logger.info("macOS input controller initialized")
        except ImportError as e:
            logger.error(f"Failed to import Quartz: {e}")

    def move_mouse(self, x: int, y: int) -> None:
        """Move mouse to absolute position."""
        try:
            from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap
            from Quartz import CGEventMovedMouse
            
            event = CGEventCreateMouseEvent(None, CGEventMovedMouse, (int(x), int(y)), 0)
            CGEventPost(kCGHIDEventTap, event)
        except Exception as e:
            logger.error(f"Failed to move mouse: {e}")

    def click_left(self) -> None:
        """Left mouse click."""
        try:
            from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap
            from Quartz import CGEventLeftMouseDown, CGEventLeftMouseUp
            
            pos = self.get_mouse_position()
            event_down = CGEventCreateMouseEvent(None, CGEventLeftMouseDown, (pos.x, pos.y), 0)
            CGEventPost(kCGHIDEventTap, event_down)
            
            event_up = CGEventCreateMouseEvent(None, CGEventLeftMouseUp, (pos.x, pos.y), 0)
            CGEventPost(kCGHIDEventTap, event_up)
        except Exception as e:
            logger.error(f"Failed to click left: {e}")

    def click_right(self) -> None:
        """Right mouse click."""
        try:
            from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap
            from Quartz import CGEventRightMouseDown, CGEventRightMouseUp
            
            pos = self.get_mouse_position()
            event_down = CGEventCreateMouseEvent(None, CGEventRightMouseDown, (pos.x, pos.y), 0)
            CGEventPost(kCGHIDEventTap, event_down)
            
            event_up = CGEventCreateMouseEvent(None, CGEventRightMouseUp, (pos.x, pos.y), 0)
            CGEventPost(kCGHIDEventTap, event_up)
        except Exception as e:
            logger.error(f"Failed to click right: {e}")

    def click_middle(self) -> None:
        """Middle mouse click."""
        try:
            from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap
            from Quartz import CGEventOtherMouseDown, CGEventOtherMouseUp
            
            pos = self.get_mouse_position()
            event_down = CGEventCreateMouseEvent(None, CGEventOtherMouseDown, (pos.x, pos.y), 2)
            CGEventPost(kCGHIDEventTap, event_down)
            
            event_up = CGEventCreateMouseEvent(None, CGEventOtherMouseUp, (pos.x, pos.y), 2)
            CGEventPost(kCGHIDEventTap, event_up)
        except Exception as e:
            logger.error(f"Failed to click middle: {e}")

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Scroll wheel."""
        try:
            from Quartz import CGEventCreateScrollWheelEvent, CGEventPost, kCGHIDEventTap
            
            if delta_y != 0:
                event = CGEventCreateScrollWheelEvent(None, 1, 1, int(delta_y))
                CGEventPost(kCGHIDEventTap, event)
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")

    def get_mouse_position(self) -> MousePosition:
        """Get current mouse position."""
        try:
            from Quartz import CGEventCreate
            
            event = CGEventCreate(None)
            pos = (0, 0)  # Placeholder - actual implementation depends on framework
            return MousePosition(x=int(pos[0]), y=int(pos[1]))
        except Exception as e:
            logger.error(f"Failed to get mouse position: {e}")
            return MousePosition(x=0, y=0)

    def release_all_buttons(self) -> None:
        """Release all mouse buttons."""
        pass


class LinuxInputController(InputController):
    """Input controller for Linux systems using xdotool."""

    def __init__(self):
        """Initialize Linux input controller."""
        try:
            import subprocess
            self.subprocess = subprocess
            logger.info("Linux input controller initialized")
        except ImportError:
            logger.error("Failed to import subprocess for Linux")

    def _run_command(self, cmd: list) -> bool:
        """Run system command."""
        try:
            self.subprocess.run(cmd, check=True, capture_output=True)
            return True
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return False

    def move_mouse(self, x: int, y: int) -> None:
        """Move mouse to absolute position."""
        self._run_command(['xdotool', 'mousemove', str(int(x)), str(int(y))])

    def click_left(self) -> None:
        """Left mouse click."""
        self._run_command(['xdotool', 'click', '1'])

    def click_right(self) -> None:
        """Right mouse click."""
        self._run_command(['xdotool', 'click', '3'])

    def click_middle(self) -> None:
        """Middle mouse click."""
        self._run_command(['xdotool', 'click', '2'])

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """Scroll wheel."""
        if delta_y > 0:
            self._run_command(['xdotool', 'click', '4'])
        elif delta_y < 0:
            self._run_command(['xdotool', 'click', '5'])

    def get_mouse_position(self) -> MousePosition:
        """Get current mouse position."""
        try:
            result = self.subprocess.run(
                ['xdotool', 'getmouselocation'],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse "x:100 y:200 screen:0"
            parts = result.stdout.strip().split()
            x = int(parts[0].split(':')[1])
            y = int(parts[1].split(':')[1])
            return MousePosition(x=x, y=y)
        except Exception as e:
            logger.error(f"Failed to get mouse position: {e}")
            return MousePosition(x=0, y=0)

    def release_all_buttons(self) -> None:
        """Release all mouse buttons."""
        pass


def create_input_controller() -> InputController:
    """
    Factory function to create platform-specific input controller.
    
    Returns:
        InputController instance for current platform
        
    Raises:
        RuntimeError: If platform is not supported
    """
    if sys.platform == 'win32':
        return WindowsInputController()
    elif sys.platform == 'darwin':
        return MacOSInputController()
    elif sys.platform.startswith('linux'):
        return LinuxInputController()
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")
