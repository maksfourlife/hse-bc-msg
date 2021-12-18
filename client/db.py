from functools import wraps
import lmdb

env = lmdb.open("db")


def with_env(write: bool):
    """
    Декоратор для ускорения написания функций, работающих с lmdb.
    Инициализирует `env` и передает `txn` в декорируемую функцию
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with env.begin(write=write) as txn:
                return fn(txn, *args, **kwargs)

        return wrapper
    return decorator


@with_env(write=True)
def store_key(txn, address: str, key: bytes):
    """Сохраняет пару `address` - `key` в db"""
    # print("write", address, key)
    txn.put(address.encode(), key)


@with_env(write=False)
def load_key(txn, address: str) -> bytes:
    """Получает пару для `address` из db"""
    key = txn.get(address.encode())
    # print("read", address, key)
    return key


@with_env(write=True)
def delete_address(txn, address: str) -> bytes:
    """Удаляет пару `address` из db"""
    txn.delete(address.encode())
