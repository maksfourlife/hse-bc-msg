from client.inbox import *


account.address = "0xBdedBED81C6D7ceBDeDfFaecDeBd12063AF4f4fB"


def test_message_out_of_bounds_reverts():
    """Проверяет, что обращение к сообщению вне границ вызывывает исключение"""

    count = Inbox.count()
    
    try:
        Inbox.load(count)
    except KeyError:
        return


def test_message_in_bounds_returns():
    """Проверяет, что обращение в границах контракта возвращает сообщение"""

    count = Inbox.count()
    Inbox.load(count - 1)
