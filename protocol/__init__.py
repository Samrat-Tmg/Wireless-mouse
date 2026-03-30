"""Protocol module for Touchpad."""
from .constants import MessageType, GestureType, PROTOCOL_VERSION
from .serialization import ProtocolSerializer

__all__ = [
    'MessageType',
    'GestureType',
    'PROTOCOL_VERSION',
    'ProtocolSerializer',
]
