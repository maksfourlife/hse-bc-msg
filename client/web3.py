from typing import Dict
from web3 import Web3, WebsocketProvider
import json

from client.args import args


CONTRACT_ABI = "contracts/MessageStorage.abi.json"
CONTRACT_ADDRESS = "0xC65E7E9B9cC36fF446B932653Ff8574692E4CB49"

web3 = Web3(WebsocketProvider(args.ws))

with open(CONTRACT_ABI, "r") as fp:
    abi = json.load(fp)

contract = web3.eth.contract(CONTRACT_ADDRESS, abi=abi)


def send_transaction(txn: Dict) -> str:
    txn["gasPrice"] = args.gasprice
    raw = web3.eth.acount.sign_transaction(txn, args.secret)
    return web3.eth.send_raw_transaction(raw)
