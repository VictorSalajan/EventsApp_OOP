from datetime import datetime
from dataclasses import dataclass


@dataclass
class Event:
    __id: int
    __date: datetime
    __time: int
    __description: str

    @property
    def id(self):
        return self.__id

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
class Person:
    __id: int
    __name: str
    __address: str

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address

@dataclass
class Enrollment:
    __event_id: int
    __person_id: int

    @property
    def event_id(self):
        return self.__event_id

    @property
    def person_id(self):
        return self.__person_id
