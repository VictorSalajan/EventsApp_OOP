from datetime import datetime
from dataclasses import dataclass


@dataclass
class Entity:
    __id: int

    @property
    def id(self):
        return self.__id


@dataclass
class Event(Entity):                    # super called automatically
    __date: datetime
    __time: int
    __description: str

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time

    @property
    def description(self):
        return self.__description


@dataclass
class Person(Entity):
    __name: str
    __address: str

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address


@dataclass                  # this is not similar enough to Entity to inherit from it
class Enrollment:
    __event_id: int
    __person_id: int

    @property
    def event_id(self):
        return self.__event_id

    @property
    def person_id(self):
        return self.__person_id
