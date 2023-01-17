from domain.exceptions.duplicate_error import DuplicateError


class EnrollmentRepository:
    def __init__(self, event_repository, person_repository):
        self.__enrollments = []
        self.__event_repository = event_repository
        self.__person_repository = person_repository

    def save(self, enrollment):
        """
        Adauga o inscriere in lista de inscrieri
        :param enrollment: obiect de tip Enrollment
        :return:
        """
        event_id = enrollment.event_id
        person_id = enrollment.person_id
        events = self.__event_repository
        persons = self.__person_repository
        if events.find_by_id(event_id) is None or persons.find_by_id(person_id) is None:
            raise KeyError("Event or person with given ids do not exist!")

        if self.find_by_event_id_and_person_id(event_id, person_id):
            raise DuplicateError("Person is already enrolled in this event!")

        self.__enrollments.append(enrollment)

    def find_all(self):     # does not include enrollments where person or event are None
        """
        Returneaza toate obiectele de tip Enrollment prezenta in lista de inscrieri
        :return: lista de obiecte de tip Enrollment
        """
        return self.__enrollments

    def find_by_event_id_and_person_id(self, event_id, person_id):
        """
        Gaseste o inscriere dupa id-urile evenimentului si persoanei asociate
        :param event_id: int
        :param person_id: int
        :return: obiect de tip Enrollment
        """
        for enrollment in self.find_all():
            if enrollment.event_id == event_id and enrollment.person_id == person_id:
                return enrollment
        return None

    def delete_by_event_id_and_person_id(self, event_id, person_id):
        """
        Sterge o inscriere din lista de inscrieri
        :param event_id: int
        :param person_id: int
        :return:
        """
        if self.find_by_event_id_and_person_id(event_id, person_id) is None:
            raise KeyError("No enrollment with given event and person ids was found.")

        i = 0
        while i < len(self.__enrollments):
            if self.__enrollments[i].event_id == event_id and self.__enrollments[i].person_id == person_id:
                self.__enrollments.pop(i)
                break                       # no need for i--; deletes just one object
            i = i + 1
