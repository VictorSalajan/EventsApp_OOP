from repository.enrollments_repository import EnrollmentRepository
from domain.entities import Person
from repository.generic_repo import Repository


class PersonService:
    def __init__(self, person_repository: Repository, enrollment_repository: EnrollmentRepository):
        self.__person_repository = person_repository
        self.__enrollment_repository = enrollment_repository

    def find_all(self):
        """
        Returneaza o lista de persoane
        :return: list of objects of type Person
        """
        return self.__person_repository.find_all()

    def save(self, person_id, name, address):
        """
        Adauga o persoana
        :param person_id: int
        :param name: string
        :param address: string
        :return:
        """
        person = Person(person_id, name, address)
        self.__person_repository.save(person)

    def update(self, person_id, name, address):
        """
        Modifica o persoana
        :param person_id: int
        :param name: string
        :param address: string
        :return:
        """
        new_person = Person(person_id, name, address)
        self.__person_repository.update(new_person)

    def delete_by_id(self, person_id):
        """
        Sterge o persoana dupa id
        :param person_id: int
        :return:
        """
        enrollments = self.__enrollment_repository.find_all()

        i = 0
        while i < len(enrollments):                     # cascade delete
            if enrollments[i].person_id == person_id:
                event_id = enrollments[i].event_id
                self.__enrollment_repository.delete_by_event_id_and_person_id(event_id, person_id)
                i = i - 1
            i = i + 1

        self.__person_repository.delete_by_id(person_id)

    def find_all_by_string_in_name(self, string):
        """
        Returneaza toate persoanele care au o secventa de caractere in nume
        :param string: str
        :return: lista de obiecte de tip Person
        """
        persons = self.find_all()
        matches = []
        for person in persons:
            if string in person.name:
                matches.append(person)
        return matches
