from repository.enrollments_repository import EnrollmentRepository
from repository.events_repository import EventRepository
from domain.entities import Event


class EventService:
    def __init__(self, event_repository: EventRepository, enrollment_repository: EnrollmentRepository):
        self.__event_repository = event_repository
        self.__enrollment_repository = enrollment_repository

    def find_all(self):
        """
        Returneaza o lista de evenimente
        :return: list of objects of type Event
        """
        return self.__event_repository.find_all()

    def save(self, event_id, date, time, description):
        """
        Adauga un eveniment
        :param event_id: int
        :param date: datetime
        :param time: int
        :param description: string
        :return:
        """
        event = Event(event_id, date, time, description)
        self.__event_repository.save(event)

    def update(self, event_id, date, time, description):
        """
        Modifica un eveniment dupa id
        :param event_id: int
        :param date: datetime
        :param time: int
        :param description: string
        :return:
        """
        new_event = Event(event_id, date, time, description)
        self.__event_repository.update(new_event)

    def delete_by_id(self, event_id):
        """
        Sterge un eveniment dupa id
        :param event_id: int
        :return:
        """
        enrollments = self.__enrollment_repository.find_all()

        i = 0
        while i < len(enrollments):                 # cascade delete
            if enrollments[i].event_id == event_id:
                person_id = enrollments[i].person_id
                self.__enrollment_repository.delete_by_event_id_and_person_id(event_id, person_id)
                i = i - 1
            i = i + 1
        self.__event_repository.delete_by_id(event_id)

    def find_all_by_words_in_description(self, words):
        """
        Returneaza evenimentele dupa cuvinte in descriere, case insensitive
        :param words: list of strings
        :return: lista de obiecte de tip Event
        """
        words = words.lower().split()
        events = self.find_all()
        matches = []
        for event in events:
            words_found = True
            for word in words:
                if word not in event.description.lower().split():
                    words_found = False
                    break
            if words_found:
                matches.append(event)
        return matches
