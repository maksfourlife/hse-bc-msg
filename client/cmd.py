from cmd import Cmd


class MsgCmd(Cmd):
    def do_request(self, arg):
        """Отправляет запрос на переписку на адрес: request 0x0..0"""
        raise NotImplemented
    
    def do_accept(self, arg):
        """Принимает запрос на переписку от адреса: accept 0x0..0"""
        raise NotImplemented
    
    def do_msg(self, arg):
        """Отправляет сообщение в переписку по адресу: msg 0x0..0 \"Hello, my...\""""
        raise NotImplemented
