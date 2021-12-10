from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


@dataclass
class Message:
    class MessageType(Enum):
        Request = auto()
        Accept = auto()
        Msg = auto()
    
    _type: MessageType
    content: bytes
    receiver: bytes
    sender: Optional[bytes]
    timestamp: Optional[int]
