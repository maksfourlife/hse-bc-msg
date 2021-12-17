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
    "-gasprice",
    help="цена газа",
    required=False
)

args = parser.parse_args()
