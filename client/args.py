from argparse import ArgumentParser


parser = ArgumentParser(
    usage="P2P мессенджер для обмена сообщениями на EVM блокчейнах"
)

parser.add_argument(
    "-secret",
    help="приватный ключ кот кошелька",
    required=True
)

parser.add_argument(
    "-rpc",
    help="rpc для доступа к сети",
    default="https://polygon-rpc.com"
)

parser.add_argument(
    "-gasprice",
    help="цена газа",
    required=False,
    default=40000000000
)

ARGS = parser.parse_args()
