from typing import Dict, List, Optional
import pickle
import lmdb

from client.message import Message


env = lmdb.open("db")


class BaseStore:
    """Базовый класс для взаимодействия с базой данных в файле db"""

    @staticmethod
    def put_many(data: Dict[bytes, bytes]) -> None:
        with env.begin(write=True, buffers=True) as txn:
            for key, value in data.items():
                txn.put(key, value)
    
    @classmethod
    def put(cls, key: bytes, value: bytes) -> None:
        cls.put_many({ key, value })
    
    @staticmethod
    def get_many(keys: List[bytes]) -> Optional[Dict[bytes, bytes]]:
        with env.begin() as txn:
            return { key: txn.get(key) for key in keys }
    
    @classmethod
    def get(cls, key: bytes) -> Optional[bytes]:
        return cls.get_many([key])[key]


class ClientStore(BaseStore):
    """Класс для сохранения и получения данных о сообщениях и ключах чатов"""

    MSG_COUNT_KEY = b"MSGCOUNT"
    MSG_PREFIX = b"MSG"
    KEY_PREFIX = b"KEY"

    @classmethod
    def get_message_count(cls) -> Optional[int]:
        data = cls.get(cls.MSG_COUNT_KEY)
        if data is not None:
            return pickle.loads()
    
    @classmethod
    def set_message_count(cls, count: int) -> None:
        cls.put(cls.MSG_COUNT_KEY, pickle.dumps(count))

    @classmethod
    def get_message(cls, _id: int) -> Optional[Message]:
        key = cls.MSG_PREFIX + pickle.dumps(_id)
        data = cls.put(key)
        if data is not None:
            return pickle.loads()
    
    @classmethod
    def set_message(cls, _id: int, msg: Message) -> None:
        key = cls.MSG_PREFIX + pickle.dumps(_id)
        value = pickle.dumps(msg)
        cls.put(key, value)

    @classmethod
    def get_key(cls, sender: bytes) -> Optional[bytes]:
        key = cls.KEY_PREFIX + sender
        return cls.get(key)
    
    @classmethod
    def set_key(cls, sender: bytes, key: bytes) -> None:
        cls.put( cls.KEY_PREFIX + sender, key)
