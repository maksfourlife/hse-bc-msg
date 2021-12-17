from cmd import Cmd


class MsgCmd(Cmd):
    currenct_chat = None

    def do_request(self, arg):
        """Отправляет запрос на переписку на адрес: request 0x0..0"""
        # raise NotImplemented
        print("request")
    
    def do_accept(self, arg):
        """Принимает запрос на переписку от адреса: accept 0x0..0"""
        # raise NotImplemented
        print("accept")

    def do_open(self, arg):
        """Открывает переписку с адресом 0x0..0"""
        # Устанавливается переменная {current_chat = 0x0000 | NONE} что открыт чат на адрес
        raise NotImplemented

    def do_close(self, arg):
        """Закрывает чат"""
        raise NotImplemented

    def do_msg(self, arg):
        """Отправляет сообщение в переписку по адресу: msg 0x0..0 \"Hello, my...\""""
        # currenct_chat != None
        # raise NotImplemented
        print("msg")

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

