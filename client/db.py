from functools import wraps
import pickle
from typing import Any, Generator, List
import lmdb
from rsa.key import PublicKey

env = lmdb.open("db")


def with_env(write: bool):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with env.begin(write=write) as txn:
                return fn(txn, *args, **kwargs)

        return wrapper
    return decorator


@with_env(write=True)
def store_key(txn, address: str, key: bytes):
    txn.put(address.encode(), key)


@with_env(write=False)
def load_key(txn, address: str) -> bytes:
    return txn.get(address.encode())


@with_env(write=True)
def store_message(txn, id: int, message):
    txn.put(f"MSG{id}".encode(), pickle.dumps(message))


@with_env(write=False)
def load_message(txn, id: int):
    return pickle.loads(txn.get(f"MSG{id}".encode()))


@with_env(write=False)
def list_messages(txn) -> Generator[Any, None, None]:
    for key, value in txn.cursor():
        if key.startswith(b"MSG"):
            yield [int(key[3:].encode()), pickle.loads(value)]
