from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Generator, List, Optional
from Crypto.Cipher import AES
from web3.exceptions import ContractLogicError
from threading import Thread
from time import sleep
import rsa
import secrets

from client.db import load_key, store_key
from client.web3 import contract, send_transaction
from client.args import args
from client.web3 import web3, account


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


class Message(Message):
    @staticmethod
    def _from_payload(payload: List) -> Message:
        _type, content, sender, timestamp = payload

        return Message(
            Message.MessageType(_type),
            content,
            sender=sender,
            timestamp=timestamp
        )

    @staticmethod
    def count() -> int:
        return contract.functions.messageCount(account.address).call()

    @staticmethod
    def load(_id: int) -> Message:
        try:
            payload = contract.functions.messages(account.address, _id).call()
        except ContractLogicError:
            raise KeyError(_id)

        return Message._from_payload(payload)

    @staticmethod
    def load_range(rng: range) -> Generator[Message, None, None]:
        for _id in rng:
            yield Message.load(_id)

    @staticmethod
    def load_last(sender: str) -> Optional[Message]:
        sender = web3.toChecksumAddress(sender)

        count = contract.functions.messageCount(account.address).call()

        for message in Message.load_range(range(count)[::-1]):
            if message.sender == sender:
                return message

    def send(self) -> str:
        assert self.receiver, "Message shoud contain receiver to be sent"
        
        sendMessage = contract.functions.sendMessage(
            self._type.value,
            self.content,
            web3.toChecksumAddress(self.receiver)
        )

        txn = {
            "chainId": 137,
            "to": contract.address,
            "data": sendMessage._encode_transaction_data(),
            "nonce": web3.eth.get_transaction_count(account.address)
        }

        txn["gas"] = web3.eth.estimate_gas(txn) * 2
        txn["gasPrice"] = args.gasprice
        
        raw = account.sign_transaction(txn)["rawTransaction"]
        return web3.eth.send_raw_transaction(raw).hex()



POLLING_INTERVAL = 10

MessageListener = Callable[[List[Message]], None]

