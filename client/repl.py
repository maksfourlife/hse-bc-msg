class Repl:
    current_chat = None

    @classmethod
    def help(cls):
        """Помощь по коммандам"""
        for cmd, fn in cls.handlers.items():
            print(f"{cmd}: {fn.__doc__}")

    @classmethod
    def quit(cls):
        """Завершает работу приложения"""
        exit(0)

    @classmethod
    def open(cls, address: str):
        """Откарывает чат с адресом `address`"""
        pass


    handlers = {
        "help": help.__func__,
        "quit": quit.__func__,
        "open": open.__func__
    }

    @classmethod
    def start(cls):
        while True:
            if cls.current_chat is not None:
                print(f"({cls.current_chat})")
            cmd, *args = input("> ").split()

            handler = cls.handlers.get(cmd, None)

            if handler is None:
                print(f"unknown command: {cmd}")
            else:
                try:
                    handler(cls, *args)
                except Exception as e:
                    print(e)
