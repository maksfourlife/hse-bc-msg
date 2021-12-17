from dataclasses import dataclass
from enum import Enum, auto
import json
from typing import Any, List, Optional
from web3 import Web3
from web3.providers.rpc import HTTPProvider

from client.crypto import create_key_pair, create_symmetric_key, encode_message
from client.args import args


ENDPOINT = "https://polyon-rpc.com"
CONTRACT_ABI = "contracts/MessageStorage.abi.json"
CONTRACT_ADDRESS = "0xC65E7E9B9cC36fF446B932653Ff8574692E4CB49"

web3 = Web3(HTTPProvider(ENDPOINT))

with open(CONTRACT_ABI, "r") as fp:
    abi = json.loads(fp)

contract = web3.eth.contract(CONTRACT_ADDRESS, abi=abi)


@dataclass
class Message:
    class MessageType(Enum):
        Request = auto()
        Accept = auto()
        Text = auto()
    
    _type: MessageType
    content: bytes
    receiver: bytes
    sender: Optional[bytes]
    timestamp: Optional[int]


class Message(Message):
    @staticmethod
    def make_request_message(receiver: bytes) -> Message:
        pub, priv = create_key_pair()
        # store_key(receiver, priv)

        return Message(
            Message.MessageType.Request,
            pub.save_pks1(),
            receiver
        )

    @staticmethod
    def make_accept_message(receiver: bytes) -> Message:
        # pub = load_key(receiver)
        pub = None
        key = create_symmetric_key()
        content = encode_message(key, pub)

        return Message(
            Message.MessageType.Accept,
            content,
            receiver
        )

    @staticmethod
    def make_text_message(receiver: bytes, text: bytes) -> Message:
        key = None
        # key = load_key(receiver)
        content = encode_message(text, key)

        return Message(
            Message.MessageType.Text,
            content,
            receiver
        )

    @staticmethod
    def _from_payload(payload: List) -> Message:
        _type, content, receiver, sender, timestamp = payload

        receiver = bytes.fromhex(receiver[2:])
        sender= bytes.fromhex(sender[2:])

        return Message(
            _type,
            content,
            receiver,
            sender,
            timestamp
        )

    @staticmethod
    def count() -> int:
        return contract.functions.messageCount().call()

    @staticmethod
    def load(id: int) -> Message:
        payload = contract.functions.messages(id).call()
        
        if payload[3] == "0x0000000000000000000000000000000000000000":
            raise KeyError(id)
        
        return Message._from_payload(payload)

    def send(self):
        txn = contract.sendMessage(
            self._type.value, self.content, self.receiver
        ).buildTransaction()

        raw = web3.eth.acount.sign_transaction(txn, args.secret)
        web3.eth.send_raw_transaction(raw)
