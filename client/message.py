from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional
from Crypto.Cipher import AES
import rsa
import secrets

from client.db import load_key, store_key


RSA_NUM_BITS = 1024
AES_NUM_BYTES = 16


@dataclass
class Message:
    class MessageType(Enum):
        Request = auto()
        Accept = auto()
        Text = auto()
    
    _type: MessageType
    content: bytes

    receiver: Optional[str] = None
    sender: Optional[str] = None
    timestamp: Optional[int] = None


class Message(Message):
    @staticmethod
    def make_request_message(receiver: str) -> Message:
        pub, priv = rsa.newkeys(RSA_NUM_BITS)
        store_key(receiver, priv.save_pkcs1())

        return Message(
            Message.MessageType.Request,
            pub.save_pkcs1(),
            receiver
        )

    @staticmethod
    def make_accept_message(receiver: str, pub: bytes) -> Message:
        key = secrets.token_bytes(AES_NUM_BYTES)
        store_key(receiver, key)

        content = rsa.encrypt(key, rsa.PublicKey.load_pkcs1(pub))

        return Message(
            Message.MessageType.Accept,
            content,
            receiver
        )

    @staticmethod
    def make_text_message(receiver: str, text: bytes) -> Message:
        key = load_key(receiver)
        content = rsa.encrypt(text, rsa.PublicKey.load_pkcs1(key))

        return Message(
            Message.MessageType.Text,
            content,
            receiver
        )

    def decrypt(self) -> Message:
        key = load_key(self.sender)

        if self._type == Message.MessageType.Request:
            return rsa.decrypt(
                self.content,
                rsa.PrivateKey.load_pkcs1(key)
            )
        elif self._type == Message.MessageType.Text:
            cipher = AES.new(key, AES.MODE_EAX)
            return cipher.decrypt(self.content)
        else:
            raise NotImplementedError(
                f"Decryption is not impemented for "
                f"{Message.MessageType.Request} messages"
            )

    @staticmethod
    def _from_payload(payload: List) -> Message:
        _type, content, sender, timestamp = payload

        return Message(
            Message.MessageType(_type),
            content,
            sender=sender,
            timestamp=timestamp
        )
