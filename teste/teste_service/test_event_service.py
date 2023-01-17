from domain.entities import Enrollment, Person
from domain.event_validator import EventValidator
from repository.enrollments_repository import EnrollmentRepository
from service.events_service import EventService
from repository.generic_repo import Repository
from datetime import datetime
from unittest import TestCase


class TestEventService(TestCase):
    def setUp(self):
        self.event_repository = Repository()
        self.person_repository = Repository()
        self.enrollment_repository = EnrollmentRepository(self.event_repository, self.person_repository)
        self.event_validator = EventValidator()
        self.event_service = EventService(self.event_repository, self.enrollment_repository, self.event_validator)
        self.person1 = Person(1, "Ana", "Cluj")
        self.person2 = Person(2, "Mihai", "Bucuresti")
        self.event_service.save(1, datetime(day=1, month=1, year=2000), 20, "Conferinta arte plastice")
        self.event_service.save(3, datetime(day=3, month=3, year=1999), 60, "Prelegere Informatica")
        self.person_repository.save(self.person1)
        self.person_repository.save(self.person2)
        self.enrollment1 = Enrollment(1, 1)
        self.enrollment2 = Enrollment(3, 1)
        self.enrollment3 = Enrollment(3, 2)

        self.enrollment_repository.save(self.enrollment1)
        self.enrollment_repository.save(self.enrollment2)
        self.enrollment_repository.save(self.enrollment3)

    def test_save(self):
        self.event_service.save(2, datetime(day=2, month=2, year=2010), 30, "Workshop Mecanica")
        events = self.event_service.find_all()

        self.assertTrue(len(events) == 3)
        self.assertTrue(events[2].id == 2)
        self.assertTrue(events[2].date == datetime(day=2, month=2, year=2010))
        self.assertTrue(events[2].time == 30)
        self.assertTrue(events[2].description == "Workshop Mecanica")

        try:
            self.event_service.save(2, datetime(day=1, month=1, year=2000), 10, "descriere")
            self.assertRaises(KeyError, self.event_service.save(2, datetime(day=1, month=1, year=2000), 10, "descriere"), "Duplicate id")
        except KeyError:
            pass

    def test_update(self):
        self.event_service.update(1, datetime(day=2, month=2, year=2010), 30, "Workshop")
        events = self.event_service.find_all()
        self.assertTrue(events[0].id == 1)
        self.assertTrue(events[0].date == datetime(day=2, month=2, year=2010))
        self.assertTrue(events[0].time == 30)
        self.assertTrue(events[0].description == "Workshop")

        try:
            self.event_service.update(2, datetime(day=1, month=1, year=2000), 10, "descriere")
            self.assertRaises(KeyError, self.event_service.update(2, datetime(day=1, month=1, year=2000), 10, "descriere"), "Id does not exist")
        except KeyError:
            pass

    def test_find_all(self):
        events = self.event_service.find_all()
        self.assertTrue(len(events) == 2)
        self.assertTrue(events[0].id == 1)
        self.assertTrue(events[1].id == 3)

    def test_delete_by_id(self):
        self.assertTrue(len(self.event_service.find_all()) == 2)
        self.assertTrue(len(self.enrollment_repository.find_all()) == 3)
        self.event_service.delete_by_id(3)
        self.assertTrue(len(self.event_service.find_all()) == 1)
        self.assertTrue(self.event_service.find_all()[0].id == 1)
        self.assertTrue((len(self.enrollment_repository.find_all()) == 1))
        self.assertIsNotNone(self.enrollment_repository.find_by_event_id_and_person_id(1, 1))

        try:
            self.event_service.delete_by_id(3)
            self.assertRaises(KeyError, self.event_service.delete_by_id(3), "Id does not exist")
        except KeyError:
            pass

    def test_find_all_by_words_in_description(self):
        self.event_service.save(2, datetime(day=1, month=1, year=1999), 10, "informatica aplicata")
        selected_events = self.event_service.find_all_by_words_in_description('informatica')
        self.assertTrue(len(selected_events) == 2)
        selected_events = self.event_service.find_all_by_words_in_description('Informatica')
        self.assertTrue(len(selected_events) == 2)
        selected_events = self.event_service.find_all_by_words_in_description('INFOrmatica')
        self.assertTrue(len(selected_events) == 2)
        selected_events = self.event_service.find_all_by_words_in_description("Conferinta plastice")
        self.assertTrue(selected_events[0].description == "Conferinta arte plastice")

        self.assertListEqual(self.event_service.find_all_by_words_in_description('info'), [])
        self.assertListEqual(self.event_service.find_all_by_words_in_description('medicina'), [])
