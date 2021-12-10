from typing import Callable, Tuple

from client.contract import Contract, Message


class Oracle:
    def __init__(self, notify_msg: Callable[[Message], None]) -> None:
        self.notify_msg = notify_msg
        self.last_count = 0

    def check_messages(self):
        count = Contract.get_message_count()
        
        if self.last_count < count:
            for i in range(self.last_count, count):
                msg = Contract.get_message(i)
                self.notify_msg(msg)
