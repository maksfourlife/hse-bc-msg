from client.db import *


def test_store_equal_load_key():
    """Проверяет, что сохраненный и полученный ключи равны"""
    address = "address"
    key = b"key"

    store_key(address, key)
    assert load_key(address) == key

    delete_address(address)


def test_unstored_key_is_none():
    """Проверяет, что обращение по не сущетвующему адресу вернет None"""

    address = "address"
    key = load_key(address)

    assert key is None
