from datetime import datetime
from domain.entities import Event, Enrollment
from repository.enrollments_repository import EnrollmentRepository
from service.persons_service import PersonService
from repository.generic_repo import Repository
from unittest import TestCase


class TestPersonService(TestCase):
    def setUp(self):
        self.event_repository = Repository()
        self.person_repository = Repository()
        self.enrollment_repository = EnrollmentRepository(self.event_repository, self.person_repository)
        self.person_service = PersonService(self.person_repository, self.enrollment_repository)

        self.event1 = Event(1, datetime(day=1, month=1, year=2000), 10, "descriere")
        self.event2 = Event(2, datetime(day=1, month=1, year=2000), 10, "descriere")
        self.person_service.save(1, "Ana Maria Ionescu", "Cluj")
        self.person_service.save(2, "Anamaria Popescu", "Bucuresti")
        self.event_repository.save(self.event1)
        self.event_repository.save(self.event2)

        self.enrollment1 = Enrollment(1, 1)
        self.enrollment2 = Enrollment(1, 2)
        self.enrollment3 = Enrollment(2, 2)
        self.enrollment_repository.save(self.enrollment1)
        self.enrollment_repository.save(self.enrollment2)
        self.enrollment_repository.save(self.enrollment3)

    def test_save(self):
        self.person_service.save(3, "Mihai Ionescu", "Brasov")
        self.assertTrue(len(self.person_service.find_all()) == 3)
        self.assertTrue(self.person_service.find_all()[2].id == 3)

        try:
            self.person_service.save(3, "Nume", "adresa")
            self.assertRaises(KeyError, self.person_service.save(3, "Nume", "adresa"), "Duplicate id")
        except KeyError:
            pass

    def test_update(self):
        self.person_service.update(2, "Mihai Ionescu", "Adresa noua")
        persons = self.person_service.find_all()
        self.assertTrue(persons[1].id == 2)
        self.assertTrue(persons[1].name == "Mihai Ionescu")
        self.assertTrue(persons[1].address == "Adresa noua")

        try:
            self.person_service.update(3, "nume", "adresa")
            self.assertRaises(KeyError, self.person_service.update(3, "nume", "adresa"), "Id does not exist")
        except KeyError:
            pass

    def test_find_all(self):
        persons = self.person_service.find_all()
        self.assertTrue(len(persons) == 2)
        self.assertTrue(persons[0].id == 1)
        self.assertTrue(persons[1].id == 2)

    def test_delete_by_id(self):
        self.assertTrue(len(self.person_service.find_all()) == 2)
        self.assertTrue(len(self.enrollment_repository.find_all()) == 3)
        self.person_service.delete_by_id(2)
        self.assertTrue(len(self.person_service.find_all()) == 1)
        self.assertTrue(self.person_service.find_all()[0].id == 1)

        self.assertTrue(len(self.enrollment_repository.find_all()) == 1)
        self.assertIsNotNone(self.enrollment_repository.find_by_event_id_and_person_id(1, 1))

        try:
            self.person_service.delete_by_id(2)
            self.assertRaises(KeyError, self.person_service.delete_by_id(2), "Id does not exist")
        except KeyError:
            pass

    def test_find_all_by_string_in_name(self):
        self.person_service.save(3, "George Ionescu", "adresa")
        selected_persons = self.person_service.find_all_by_string_in_name("Ionescu")
        self.assertTrue(len(selected_persons) == 2)
        self.assertTrue(selected_persons[0].id == 1)
        self.assertTrue(selected_persons[1].id == 3)
        selected_persons = self.person_service.find_all_by_string_in_name("Ana")
        self.assertTrue(len(selected_persons) == 2)
        self.assertTrue(selected_persons[0].name == "Ana Maria Ionescu")
        self.assertTrue(selected_persons[1].name == "Anamaria Popescu")
        selected_persons = self.person_service.find_all_by_string_in_name("Maria")
        self.assertTrue(len(selected_persons) == 1)
        self.assertTrue(selected_persons[0].name == "Ana Maria Ionescu")

        self.assertListEqual(self.person_service.find_all_by_string_in_name("Georgescu"), [])
