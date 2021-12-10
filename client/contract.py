from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
import eth_abi
from eth_typing.evm import Address
from web3 import Web3, HTTPProvider
from args import args


web3 = Web3(HTTPProvider(args.rpc))


@dataclass
class Message:
    class MessageType(Enum):
        Request = auto()
        Accept = auto()
        Msg = auto()
    
    _type: MessageType
    content: bytes
    receiver: Address
    sender: Optional[Address]
    timestamp: Optional[int]


class Contract:
    @staticmethod
    def get_message_count() -> int:
        """Возвращает кол-во транзакций на контракте"""
        # 0x3dbcc8d1
        # keccak256(messageCount)

        res = web3.eth.call({
            "to": args.contract,
            "data": b"\x3d\xbc\xc8\xd1"
        })

        return eth_abi.decode_abi(["uint"], res)[0]

    @staticmethod
    def get_message(_id: int) -> Message:
        """Возвращает объект сообщения по индексу"""
        # 0xcad3e16c
        # keccak256(messages(uint))

        res = web3.eth.call({
            "to": args.contract,
            "data": b"\xca\xd3\xe1\x6c" + eth_abi.encode_abi(["uint"], [_id])
        })

        types = ["uint8", "bytes", "address", "address", "uint"]
        params = eth_abi.decode_abi(types, res)
        
        return Message(*params)
    
    @staticmethod
    def send_message(msg: Message) -> None:
        # 0xa32d6cb1
        # keccak256(sendMessage(uint8,bytes,address))

        types = ["uint8", "bytes", "address"]
        params = [msg._type, msg.content, msg.receiver]

        txn = {
            "to": args.contract,
            "data": b"\xa3\x2d\x6c\xb1" + \
                eth_abi.encode_abi(types, params),
        }

        txn["gas"] = web3.eth.estimate_gas(txn)
        txn["gasPrice"] = args.gasprice or web3.eth.generate_gas_price(txn)

        
        account = web3.eth.account.privateKeyToAccount(args.secret)
        txn["nonce"] = web3.eth.get_transaction_count(account.address)

        raw_transaction = account.sing_transaction(txn)
        web3.eth.send_raw_transaction(raw_transaction)
