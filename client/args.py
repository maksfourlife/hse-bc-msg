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
    default=None
)

parser.add_argument(
    "-gasprice",
    help="цена за газ",
    default=40000000000
)

RPC = "https://polygon-rpc.com"
ARGS = None

if __name__ == "__main__":
    ARGS = parser.parse_args()
    RPC = RPC or ARGS.rpc
