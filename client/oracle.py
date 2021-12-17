from typing import Callable
from threading import Thread
from time import sleep

from client.message import Message
from client.store import ClientStore


class Oracle(Thread):
    """Ищет новые транзакции на контракте"""

    def __init__(self, notify_msg: Callable[[Message], None], poll_latency: int = 10) -> None:
        """Ищет новые транзакции с интервалом `poll_latency` и вызывает `notify_msg` при обнаружении"""
        Thread.__init__(self, daemon=True)

        self.notify_msg = notify_msg
        self.poll_latency = poll_latency

    def run(self):
        while True:
            last_count = ClientStore.get_message_count() or 0
            count = Contract.get_message_count()
            
            if last_count < count:
                for i in range(self.last_count, count):
                    msg = Contract.get_message(i)
                    ClientStore.set_message(i, msg)
                    self.notify_msg(msg)

            ClientStore.set_message_count(count)
            sleep(self.poll_latency)
