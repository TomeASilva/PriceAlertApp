from abc import ABCMeta, abstractmethod
from common.database import Database
from typing import List, TypeVar, Type, Dict, Union


class Model(metaclass=ABCMeta):
    # You will never be able to instatiate an object of class method
    # because this class has an abstract method in it
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    def save_to_database(self) -> None:
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_database(self) -> None:
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_element_by_id(cls, _id: str):
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls):

        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls, attribute: str, value: Union[str, Dict]):

        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls, attribute: str, value: Union[str, Dict]):

        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
