from cmd import Cmd
from enum import Enum, auto
from typing import Optional


from client.web3 import contract, account
from client.db import load_key

from client.message import Message



class MsgCmd(Cmd):
    class ReplMode(Enum):
        Global = auto()
        Chat = auto()
    
    def set_promt(self, mode: ReplMode):
        if mode == MsgCmd.ReplMode.Global:
            self.prompt = "command > "
        elif mode == MsgCmd.ReplMode.Chat:
            self.prompt = "msg > "

    def set_chat(self, chat: Optional[str]):
        if chat is None:
            self.current_chat = None
            self.set_promt(MsgCmd.ReplMode.Global)
        else:
            self.current_chat = chat
            self.set_promt(MsgCmd.ReplMode.Chat)

    def __init__(self):
        super().__init__()

        self.set_chat(None)

    def do_request(self, receiver):
        """Отправляет запрос на переписку на адрес: request 0x0..0"""
        
        message = Message.make_request_message(receiver)
        print(message.send())

    def do_accept(self, receiver):
        """Принимает запрос на переписку от адреса: accept 0x0..0"""

        last = Message.load_last(account.address, receiver)

        if last is None:
            print("От отправителя нет сообщений")
        elif last._type != Message.MessageType.Request:
            print("Отправитель не отправлял запрос")
        else:
            message = Message.make_accept_message(receiver, last.content)
            print(message.send())

    def do_open(self, address):
        """Открывает переписку с адресом 0x0..0"""

        if load_key(address) is None:
            print(f"Нет активного чата с адресом {address}")
        else:
            self.set_chat(address)
            count = contract.functions.messageCount(account.address).call()
            print(count)

    def do_close(self, arg):
        """Закрывает чат"""

        if self.current_chat is None:
            print("Чат не открыт")
        else:
            self.set_chat(None)

    def do_msg(self, text):
        """Отправляет сообщение в переписку по адресу: msg 0x0..0 \"Hello, my...\""""

        if self.current_chat is None:
            print("Чат не открыт")
        else:
            print(send_message("make_text_message", self.current_chat, text))

    def do_up(self, arg):
        """Пролистывает чат вверх"""
        # Обращение к базе сообщений отправленных на адрес
        # Обрещение к базе ключ-адрес

        # БАЗА КЛЮЧ_АДРЕС
        #   0xdead..00: djshascbashj
        #   address: 
        
        # 0xdead..0
        #   myaddress: djshascbashj

        raise NotImplemented
    
    def do_down(self, arg):
        """Пролистывает вниз"""
        raise NotImplemented

    def do_q(self, arg):
        """Закрывает сеанс"""
        exit(0)
