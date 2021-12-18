from cmd import Cmd
from functools import wraps
from threading import current_thread

from client.message import Message


def send_message(fn: str, receiver: str, *args) -> str:
    return getattr(Message, fn)(receiver, *args).send()


class MsgCmd(Cmd):
    current_chat = None


    def do_request(self, receiver):
        """Отправляет запрос на переписку на адрес: request 0x0..0"""
        
        print(send_message("make_request_message"), receiver)

    def do_accept(self, receiver):
        """Принимает запрос на переписку от адреса: accept 0x0..0"""

        print(send_message("make_accept_message"), receiver)

    def do_open(self, address):
        """Открывает переписку с адресом 0x0..0"""
        # Устанавливается переменная {current_chat = 0x0000 | NONE} что открыт чат на адрес
        self.current_chat = address
        # Вывести первое сообщение

    def do_close(self, arg):
        """Закрывает чат"""
        self.current_chat = None

    def do_msg(self, text):
        """Отправляет сообщение в переписку по адресу: msg 0x0..0 \"Hello, my...\""""

        if self.current_chat is None:
            print("Откройте чат")
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

