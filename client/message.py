from dataclasses import dataclass
from enum import Enum
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
        Request = 0
        Accept = 1
        Text = 2
    
    _type: MessageType
    content: bytes

    receiver: Optional[str] = None
    sender: Optional[str] = None
    timestamp: Optional[int] = None


class Message(Message):
    @staticmethod
    def make_request_message(receiver: str) -> Message:
        """
        Первое сообщение, для инициализации диалога.
        Сохраняет для ключа `receiver` созданный здесь RSA ключ.
        """

        pub, priv = rsa.newkeys(RSA_NUM_BITS)
        store_key(receiver, priv.save_pkcs1())

        return Message(
            Message.MessageType.Request,
            pub.save_pkcs1(),
            receiver
        )

    @staticmethod
    def make_accept_message(receiver: str, pub: bytes) -> Message:
        """
        Второе сооющение для иницализации диалога.
        Сохраняет для ключа `receiver` созданный здесь симметричный ключ.
        Сообщение несет данный ключ, зашифрованный с помощью `pub`.
    
        :param pub: публичный ключ в pkcs1 формат из сообщения Request
        """
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
        """
        Создает сообщение, содержащее `text`,
        зашифрованное с помощью сохраненного симметричного ключа.
        """
        key = load_key(receiver)
        cipher = AES.new(key, AES.MODE_EAX)
        content = cipher.nonce + cipher.encrypt(text)

        return Message(
            Message.MessageType.Text,
            content,
            receiver
        )

    def decrypt(self) -> bytes:
        """
        Расшифровывает контент сообщения типа Accept и Text, соответсвенно, с помощью
        приватного ключа rsa и симметричного ключа
        """
        key = load_key(self.sender)

        if self._type == Message.MessageType.Accept:
            return rsa.decrypt(
                self.content,
                rsa.PrivateKey.load_pkcs1(key)
            )
        elif self._type == Message.MessageType.Text:
            cipher = AES.new(key, AES.MODE_EAX, nonce=self.content[:AES_NUM_BYTES])
            return cipher.decrypt(self.content[AES_NUM_BYTES:])

    @staticmethod
    def _from_payload(payload: List) -> Message:
        """
        Helper для преобразования сырых данных со смарт-контракта в `Message`
        """
        _type, content, sender, timestamp = payload

        return Message(
            Message.MessageType(_type),
            content,
            sender=sender,
            timestamp=timestamp
        )
