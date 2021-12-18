from functools import wraps
import lmdb

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
    # print("write", address, key)
    txn.put(address.encode(), key)


@with_env(write=False)
def load_key(txn, address: str) -> bytes:
    key = txn.get(address.encode())
    # print("read", address, key)
    return key
