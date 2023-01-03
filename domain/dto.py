from dataclasses import dataclass


@dataclass
class EventDTO:
    description: str
    nr_of_participants: int

@dataclass()
class PersonDTO:
    name: str
    nr_of_events: int

class EventNrParticipantsDTOAssembler:
    @staticmethod
    def create_event_dto(event, event_enrollments):  # event_enrollments = list of enrollments with id of given event
        """
        Returns an EventDTO object containing the description of a given event
        and the number of participants associated with that event
        :param event: object of type Event
        :param event_enrollments: list of objects of type Enrollment
        :return: object of EventDTO
        """
        description = event.description
        nr_of_participants = len(event_enrollments)

        return EventDTO(description, nr_of_participants)

class PersonNrEventsDTOAssembler:
    @staticmethod
    def create_person_dto(person, person_enrollments):  # person_enrollments = list of enrollments with id of a given person
        """
        Returns a PersonDTO object containing the name of a given person
        and the number of events associated with that person
        :param person: object of type Person
        :param person_enrollments: list of objects of type Enrollment
        :return: object of type PersonDTO
        """
        name = person.name
        nr_of_events = len(person_enrollments)

        return PersonDTO(name, nr_of_events)
