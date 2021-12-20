from client.inbox import Inbox
from client.message import Message
from client.db import store_key


class Repl:
    """
    Статический класс для взаимодействия с пользователем.
    Все функции, кроме `start()` не предназначены для вызова пользователем.
    """

    current_chat = None

    def get_answer() -> bool:
        while True:
            x = input().lower()
            if x == "y":
                return True
            elif x == "n":
                return False

    @classmethod
    def quit(cls):
        """Завершает работу приложения"""
        exit(0)

    @classmethod
    def close(cls):
        """Закрывает открытый чат"""

        if cls.current_chat is None:
            return print("Чат не открыт")
        cls.current_chat = None
    
    @classmethod
    def reset(cls, address):
        """Сбрастывает текущий ключ шифрования в чате `address`"""
        
        print(Inbox.send_message(Message.make_request_message(address)))
    
    @classmethod
    def send_message(cls, text):
        """Отправляет сообщение в чат"""
        assert cls.current_chat is not None, "Чат не задан"

        message = Message.make_text_message(cls.current_chat, text.encode())
        print(Inbox.send_message(message))

    @classmethod
    def help(cls):
        """Помощь по коммандам"""
        for cmd, fn in cls.handlers.items():
            print(f"{cmd}: {fn.__doc__}")

    @classmethod
    def open(cls, address: str):
        """Открывает чат с адресом `address`"""
        cls.current_chat = address
        last = Inbox.load_last(address)
        
        if last is None or last.content == b"":
            print("Ключ шифрования не установлен. Послать запрос? [Y/n]", end=" ")
            if cls.get_answer():
                message = Message.make_request_message(address)
                print(Inbox.send_message(message))
            else:
                cls.close()

        elif last._type == Message.MessageType.Request:
            print("От адресa поступил запрос. Принять? [Y/n]", end=" ")
            if cls.get_answer():
                message = Message.make_accept_message(address, last.content)
                print(Inbox.send_message(message))
            cls.close()

        elif last._type == Message.MessageType.Accept:
            try:
                store_key(address, last.decrypt())
            except:
                pass # key already stored

        else:
            print(last.decrypt())
    
    handlers = {
        "help": help.__func__,
        "quit": quit.__func__,
        "open": open.__func__,
        "close": close.__func__,
        "reset": reset.__func__,
        "msg": send_message.__func__
    }

    @classmethod
    def start(cls):
        """Запускает бесконечный repl-цикл, запрашивающий пользовательский ввод"""
        while True:
            if cls.current_chat is not None:
                print(f"({cls.current_chat})")

            try:
                x = input("> ")
                if x == "":
                    continue
            except KeyboardInterrupt:
                return


            cmd, *args = x.split()

            handler = cls.handlers.get(cmd, None)

            if handler is None:
                print(f"unknown command: {cmd}")
            else:
                try:
                    handler(cls, *args)
                except Exception as e:
                    print(e)
