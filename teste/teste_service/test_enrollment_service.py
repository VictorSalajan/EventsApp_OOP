from datetime import datetime
from domain.entities import Event, Person, Enrollment
from repository.enrollments_repository import EnrollmentRepository
from repository.events_repository import EventRepository
from repository.persons_repository import PersonRepository
from service.enrollments_service import EnrollmentService
from unittest import TestCase


class TestEnrollmentService(TestCase):
    def setUp(self):
        event1 = Event(1, datetime(day=1, month=1, year=2000), 20, 'Conferinta informatica')
        event2 = Event(2, datetime(day=2, month=2, year=2010), 30, "Workshop Mecanica")
        event3 = Event(3, datetime(day=3, month=3, year=1999), 60, 'Prelegere Informatica')
        self.person1 = Person(1, 'Ana Ionescu', 'Strada Cosbuc')
        self.person2 = Person(2, "Anamaria Ionescu", "Strada Arinilor")
        self.person3 = Person(3, 'George Popescu', 'Str Arinilor')

        self.event_repository = EventRepository()
        for event in [event1, event2, event3]:
            self.event_repository.save(event)
        self.person_repository = PersonRepository()
        for person in [self.person1, self.person2, self.person3]:
            self.person_repository.save(person)

        self.enrollment_repository = EnrollmentRepository(self.event_repository, self.person_repository)
        self.enrollment_service = EnrollmentService(self.enrollment_repository, self.event_repository, self.person_repository)

        self.enrollment_service.save(1, 3)
        self.enrollment_service.save(2, 2)

    def test_save(self):
        self.enrollment_service.save(3, 1)
        self.assertTrue(len(self.enrollment_service.find_all()) == 3)
        self.assertTrue(self.enrollment_service.find_all()[2].event_id == 3)
        self.assertTrue(self.enrollment_service.find_all()[2].person_id == 1)

    def test_find_all(self):
        enrollments = self.enrollment_service.find_all()
        self.assertTrue(len(enrollments) == 2)
        self.assertTrue(enrollments[0].event_id == 1)
        self.assertTrue(enrollments[0].person_id == 3)
        self.assertTrue(enrollments[1].event_id == 2)
        self.assertTrue(enrollments[1].person_id == 2)

    def test_delete_by_event_id_and_person_id(self):
        self.assertTrue(len(self.enrollment_service.find_all()) == 2)
        self.enrollment_service.delete_by_event_id_and_person_id(2, 2)
        self.assertTrue(len(self.enrollment_service.find_all()) == 1)
        self.assertTrue(self.enrollment_service.find_all()[0].event_id == 1)
        self.assertTrue(self.enrollment_service.find_all()[0].person_id == 3)

    def test_events_by_person(self):
        self.enrollment_service.save(3, 2)
        events_by_person = self.enrollment_service.events_by_person(2)
        self.assertTrue(len(events_by_person) == 2)
        self.assertListEqual(self.enrollment_service.events_by_person(1), [])
        self.assertTrue(len(self.enrollment_service.events_by_person(3)) == 1)

    def test_events_by_person_ordered_by_description(self):
        self.enrollment_service.save(1, 2)
        self.enrollment_service.save(3, 2)
        selected_events = self.enrollment_service.events_by_person_ordered_by_description(2)
        self.assertTrue(len(selected_events) == 3)
        self.assertTrue(selected_events[0].description == "Conferinta informatica")
        self.assertTrue(selected_events[1].description == "Prelegere Informatica")
        self.assertTrue(selected_events[2].description == "Workshop Mecanica")

        selected_events = self.enrollment_service.events_by_person_ordered_by_description(3)
        self.assertTrue(len(selected_events) == 1)
        selected_events = self.enrollment_service.events_by_person_ordered_by_description(1)
        self.assertListEqual(selected_events, [])

    def test_events_by_person_ordered_by_date(self):
        self.enrollment_service.save(1, 2)
        self.enrollment_service.save(3, 2)
        selected_events = self.enrollment_service.events_by_person_ordered_by_date(2)
        self.assertTrue(len(selected_events) == 3)
        self.assertTrue(selected_events[0].date == datetime(day=3, month=3, year=1999))
        self.assertTrue(selected_events[1].date == datetime(day=1, month=1, year=2000))
        self.assertTrue(selected_events[2].date == datetime(day=2, month=2, year=2010))

    def test_persons_enrolled_in_most_events(self):
        self.enrollment_service.save(1, 2)
        self.enrollment_service.save(3, 2)
        persons_most_events = self.enrollment_service.persons_enrolled_in_most_events()
        self.assertTrue(len(persons_most_events) == 1)
        self.assertTrue(persons_most_events[0].name == "Anamaria Ionescu")
        self.assertTrue(persons_most_events[0].nr_of_events == 3)

        self.enrollment_service.delete_by_event_id_and_person_id(1, 3)
        self.enrollment_service.delete_by_event_id_and_person_id(2, 2)
        self.enrollment_service.delete_by_event_id_and_person_id(1, 2)
        self.enrollment_service.delete_by_event_id_and_person_id(3, 2)
        persons_most_events = self.enrollment_service.persons_enrolled_in_most_events()
        self.assertListEqual(persons_most_events, [])

    def test_events_with_most_participants(self):
        # test for 3 events
        self.enrollment_service.save(1, 2)
        self.enrollment_service.save(2, 1)
        self.enrollment_service.save(1, 1)
        selected_events = self.enrollment_service.events_with_most_participants(0.2)
        self.assertTrue(len(selected_events) == 1)

        self.assertTrue(selected_events[0].description == "Conferinta informatica")
        self.assertTrue(selected_events[0].nr_of_participants == 3)

        # test for 2 events, 1 with max participants
        self.event_repository.delete_by_id(3)
        selected_events = self.enrollment_service.events_with_most_participants(0.2)
        self.assertTrue(len(selected_events) == 1)
        self.assertTrue(selected_events[0].description == "Conferinta informatica")
        self.assertTrue(selected_events[0].nr_of_participants == 3)

        # 2 events with equal nr of participants
        event = Event(3, datetime(day=1, month=1, year=2000), 10, "descriere")
        self.event_repository.save(event)
        self.enrollment_service.save(3, 1)
        self.enrollment_service.save(3, 2)
        self.enrollment_service.save(3, 3)
        selected_events = self.enrollment_service.events_with_most_participants(0.2)
        self.assertTrue(len(selected_events) == 2)
        self.assertTrue(selected_events[0].description == "Conferinta informatica")
        self.assertTrue(selected_events[0].nr_of_participants == 3)
        self.assertTrue(selected_events[1].description == "descriere")
        self.assertTrue(selected_events[1].nr_of_participants == 3)

        # test for 0 events with participants (no enrollments)
        self.enrollment_service.delete_by_event_id_and_person_id(1, 3)
        self.enrollment_service.delete_by_event_id_and_person_id(2, 2)
        self.enrollment_service.delete_by_event_id_and_person_id(1, 2)
        self.enrollment_service.delete_by_event_id_and_person_id(1, 1)
        self.enrollment_service.delete_by_event_id_and_person_id(2, 1)
        self.enrollment_service.delete_by_event_id_and_person_id(3, 1)
        self.enrollment_service.delete_by_event_id_and_person_id(3, 2)
        self.enrollment_service.delete_by_event_id_and_person_id(3, 3)
        self.assertTrue(self.enrollment_service.find_all() == [])
        selected_events = self.enrollment_service.events_with_most_participants(0.2)
        self.assertListEqual(selected_events, [])
