from domain.dto import EventNrParticipantsDTOAssembler, PersonNrEventsDTOAssembler
from repository.enrollments_repository import EnrollmentRepository
from domain.entities import Enrollment
from collections import OrderedDict
from repository.generic_repo import Repository


class EnrollmentService:
    def __init__(self, enrollment_repository: EnrollmentRepository, event_repository: Repository,
                 person_repository: Repository):
        self.__enrollment_repository = enrollment_repository
        self.__event_repository = event_repository
        self.__person_repository = person_repository

    def save(self, event_id, person_id):
        """
        Adauga o inscriere in lista de inscrieri
        :param event_id: int
        :param person_id: int
        :return:
        """
        enrollment = Enrollment(event_id, person_id)
        self.__enrollment_repository.save(enrollment)

    def find_all(self):
        """
        Returneaza toate inscrierile din lista de inscrieri
        :return: lista de obiecte de tip Enrollment
        """
        return self.__enrollment_repository.find_all()

    def delete_by_event_id_and_person_id(self, event_id, person_id):
        """
        Sterge o inscriere din lista de inscrieri dupa id-urile evenimentului si persoanei
        :param event_id: int
        :param person_id: int
        :return:
        """
        self.__enrollment_repository.delete_by_event_id_and_person_id(event_id, person_id)

    def events_by_person(self, person_id):
        """
        Returneaza o lista cu evenimentele la care participa o persoana
        :param person_id: int
        :return: lista de obiecte de tip Event
        """
        person_enrollments = self.get_person_enrollments(self.__person_repository.find_by_id(person_id))
        if not person_enrollments:
            return []
        events = [self.__event_repository.find_by_id(enrollment.event_id) for enrollment in person_enrollments]
        return events

    def events_by_person_ordered_by_description(self, person_id):
        """
        Returneaza lista de evenimente la care participa o persoana, ordonate lexicografic dupa descriere
        :param person_id: int
        :return: lista de obiecte de tip Event
        """
        events = self.events_by_person(person_id)
        return sorted(events, key=lambda event: event.description)

    def events_by_person_ordered_by_date(self, person_id):
        """
        Returneaza lista de evenimente la care participa o persoana, ordonate dupa data
        :param person_id: int
        :return: lista de obiecte de tip Event
        """
        events = self.events_by_person(person_id)
        return sorted(events, key=lambda event: event.date)

    def get_person_enrollments(self, person):
        """
        Returns the enrollments associated with a given person
        :param person: object of type Person
        :return: list of objects of type Enrollment
        """
        if person is None:                               # avoids None.id error
            return []
        return [enroll for enroll in self.__enrollment_repository.find_all() if enroll.person_id == person.id]

    def create_person_dtos(self):
        """
        Creates a PersonDTO object for each person from repository
        :return: list of objects of type PersonDTO
        """
        person_dtos = []
        for person in self.__person_repository.find_all():
            enrollments = self.get_person_enrollments(person)
            person_dto = PersonNrEventsDTOAssembler.create_person_dto(person, enrollments)
            person_dtos.append(person_dto)
        return person_dtos

    def persons_enrolled_in_most_events(self):
        """
        Returneaza lista persoanelor inscrise in cele mai multe evenimente
        :return: lista de obiecte de tip Person
        """
        if len(self.__enrollment_repository.find_all()) == 0:
            return []

        person_dtos = self.create_person_dtos()
        person_dtos = sorted(person_dtos, key=lambda x: x.nr_of_events, reverse=True)

        max_events = person_dtos[0].nr_of_events
        person_dtos = [person for person in person_dtos if person.nr_of_events == max_events]

        return person_dtos

    def get_event_enrollments(self, event):
        """
        Returns the enrollments associated with a given event
        :param event: object of type Event
        :return: list of objects of type Enrollment
        """
        return [enroll for enroll in self.__enrollment_repository.find_all() if enroll.event_id == event.id]

    def create_event_dtos(self):
        """
        Creates an EventDTO object for each event from repository
        :return: list of objects of type EventDTO
        """
        event_dtos = []
        for event in self.__event_repository.find_all():
            enrollments = self.get_event_enrollments(event)               # inscrierile asociate unui eveniment
            dto = EventNrParticipantsDTOAssembler.create_event_dto(event, enrollments)
            event_dtos.append(dto)
        return event_dtos

    def events_with_most_participants(self, percent):           # percent in [0,1] range
        """
        Returns the first {percent}% of events with most participants
        :param percent: float; 0 <= percent <= 1
        :return: list of objects of type EventDTO
        """
        if self.__enrollment_repository.find_all() == []:       # no enrollments
            return []

        event_dtos = self.create_event_dtos()
        event_dtos = sorted(event_dtos, key=lambda x: x.nr_of_participants, reverse=True)
        all_events = self.__event_repository.find_all()
        nr = round(len(all_events) * percent)

        if round(len(all_events) * percent) == 0:    # too few events to extract at least one
            max_part = event_dtos[0].nr_of_participants
            top_events = [event for event in event_dtos if event.nr_of_participants == max_part]
            return top_events

        # if there are events with equal nr of participants beyond the nr of selected top events
        min_part = event_dtos[nr - 1].nr_of_participants
        equal_events = [event for event in event_dtos[nr:] if event.nr_of_participants == min_part]
        nr = nr + len(equal_events)

        return event_dtos[:nr]
