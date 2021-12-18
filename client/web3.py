from typing import Dict
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json

from client.args import args


CONTRACT_ABI = "contracts/MessageStorage.abi.json"
CONTRACT_ADDRESS = "0xc76bE499BaD3079ff49f8Ac135B673aBC3591280"

web3 = Web3(HTTPProvider(args.rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

account = web3.eth.account.privateKeyToAccount(args.secret)

with open(CONTRACT_ABI, "r") as fp:
    abi = json.load(fp)

contract = web3.eth.contract(CONTRACT_ADDRESS, abi=abi)


def send_transaction(txn: Dict) -> str:
    txn["gasPrice"] = args.gasprice
    raw = web3.eth.acount.sign_transaction(txn, args.secret)
    return web3.eth.send_raw_transaction(raw)
