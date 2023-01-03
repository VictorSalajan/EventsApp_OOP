

class EventRepository:
    def __init__(self):
        self.__events = {}

    def save(self, event):
        """
        Adauga un eveniment in dictionarul de evenimente
        :param event: object of type Event
        :return:
        """
        if self.find_by_id(event.id):
            raise KeyError("Duplicate id")
        self.__events[event.id] = event

    def update(self, event):
        """
        Modifica un eveniment dupa id
        :param event: object of type Event
        :return:
        """
        if self.find_by_id(event.id) is None:
            raise KeyError("Id does not exist")
        self.__events[event.id] = event

    def find_all(self):
        """
        Returneaza lista de evenimente
        :return: list of objects of type Event
        """
        return list(self.__events.values())

    def find_by_id(self, event_id):
        """
        Returneaza evenimentul cu un id dat
        :param event_id: int
        :return: object of type Event or None
        """
        return self.__events.get(event_id, None)

    def delete_by_id(self, event_id):
        """
        Sterge un eveniment dupa id
        :param event_id: int
        :return:
        """
        if self.find_by_id(event_id) is None:
            raise KeyError("Id does not exist")
        self.__events.pop(event_id)
