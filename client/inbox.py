from dataclasses import dataclass
from typing import Generator, Optional
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError
import json

from client.message import Message
from client.args import ARGS, RPC


@dataclass
class AccountMock:
    address: Optional[str] = None


CONTRACT_ABI = "contracts/MessageStorage.abi.json"
CONTRACT_ADDRESS = "0xc76bE499BaD3079ff49f8Ac135B673aBC3591280"

web3 = Web3(HTTPProvider(RPC))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = AccountMock()
if hasattr(ARGS, "secret"):
    account = web3.eth.account.privateKeyToAccount(ARGS.secret)

abi = json.load(open(CONTRACT_ABI))
contract = web3.eth.contract(CONTRACT_ADDRESS, abi=abi)


class Inbox:
    """Статический класс для отправки и и загрузки сообщений со смарт-конракта"""
    @staticmethod
    def send_message(message: Message) -> None:
        receiver = Web3.toChecksumAddress(message.receiver)
                
        sendMessage = contract.functions.sendMessage(
            message._type.value,
            message.content,
            receiver
        )

        txn = {
            "chainId": 137,
            "to": contract.address,
            "data": sendMessage._encode_transaction_data(),
            "nonce": web3.eth.get_transaction_count(account.address)
        }

        txn["gas"] = web3.eth.estimate_gas(txn) * 2
        txn["gasPrice"] = ARGS.gasprice
        
        raw = account.sign_transaction(txn)["rawTransaction"]
        return web3.eth.send_raw_transaction(raw).hex()

    @staticmethod
    def count() -> int:
        """
        Возвращает кол-во сообщений на адрес, соотвествующий приватному ключу,
        переданному при запуске приложения
        """
        return contract.functions.messageCount(account.address).call()

    @staticmethod
    def load(_id: int) -> Message:
        """
        Возвращает преобразованное сообщение под номером `id`,
        отправленное на адрес как в `count()`
        """
        try:
            payload = contract.functions.messages(account.address, _id).call()
        except ContractLogicError:
            raise KeyError(_id)

        return Message._from_payload(payload)

    @classmethod
    def load_range(cls, rng: range) -> Generator[Message, None, None]:
        """
        Загружает сообщения по каждому индексу из `rng`
        """
        for _id in rng:
            yield cls.load(_id)

    @classmethod
    def load_last(cls, sender: str) -> Optional[Message]:
        """
        Загружает последнее сообщение, отправленное с адреса `sender`
        """
        sender = web3.toChecksumAddress(sender)

        count = contract.functions.messageCount(account.address).call()

        for message in cls.load_range(range(count)[::-1]):
            if message.sender == sender:
                return message
