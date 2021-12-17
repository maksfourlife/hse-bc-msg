from typing import Any, Tuple

# TODO заменить типы с Any на реальные


def create_key_pair() -> Tuple[Any, Any]:
    """Создает публичный и секретный rsa ключи"""
    raise NotImplemented


def create_symmetric_key() -> Any:
    """Создает симметричный AES ключ"""
    raise NotImplemented


def encode_message(msg: bytes, key: Any) -> bytes:
    """Зашифровывает сообщение `msg` с помощью симметричного ключа `key`"""
    raise NotImplemented


def decode_message(msg: bytes, key: Any) -> bytes:
    """Расшифровывает сообщение `msg` с помощью симметричного ключа `key`"""
    raise NotImplemented
