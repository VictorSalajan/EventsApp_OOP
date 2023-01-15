from domain.entities import Enrollment, Event, Person
from repository.enrollments_repository import EnrollmentRepository
from repository.generic_repo import Repository
from datetime import datetime
from unittest import TestCase


class TestEnrollmentRepository(TestCase):
    def setUp(self):
        self.event_repository = Repository()
        self.person_repository = Repository()
        self.enrollments = EnrollmentRepository(self.event_repository, self.person_repository)

        date = datetime(day=2, month=10, year=2020)
        self.event1 = Event(1, date, 60, "descriere")
        self.event2 = Event(2, date, 30, "conferinta")
        self.event3 = Event(3, date, 90, "prelegere")
        self.event_repository.save(self.event1)
        self.event_repository.save(self.event2)
        self.event_repository.save(self.event3)

        self.person1 = Person(1, "Ana Maria", "Cluj")
        self.person2 = Person(2, "Mihai Ionescu", "Bucuresti")
        self.person3 = Person(3, "Joe Biden", "Washington")
        self.person_repository.save(self.person1)
        self.person_repository.save(self.person2)
        self.person_repository.save(self.person3)

        self.enrollment1 = Enrollment(1, 1)
        self.enrollment2 = Enrollment(2, 1)
        self.enrollment3 = Enrollment(3, 2)

        self.enrollments.save(self.enrollment1)
        self.enrollments.save(self.enrollment2)

    def test_save(self):
        self.enrollments.save(self.enrollment3)

        enrollment = self.enrollments.find_all()[2]

        self.assertTrue(enrollment.event_id == 3)
        self.assertTrue(enrollment.person_id == 2)

        try:
            enrollment = Enrollment(4, 3)
            self.enrollments.save(enrollment)
            self.assertRaises(KeyError, self.enrollments.save(enrollment), "Event with given id does not exist")
        except KeyError:
            pass

        try:
            enrollment = Enrollment(3, 4)
            self.enrollments.save(enrollment)
            self.assertRaises(KeyError, self.enrollments.save(enrollment), "Person with given id does not exist")
        except KeyError:
            pass

        try:
            enrollment = Enrollment(3, 2)
            self.enrollments.save(enrollment)
            self.assertRaises(KeyError, self.enrollments.save(enrollment), "Person is already enrolled in this event")
        except KeyError:
            pass

    def test_find_all(self):
        enrollments = self.enrollments.find_all()
        self.assertTrue(len(enrollments) == 2)
        self.assertTrue(enrollments[0].event_id == 1)
        self.assertTrue(enrollments[0].person_id == 1)
        self.assertTrue(enrollments[1].event_id == 2)
        self.assertTrue(enrollments[1].person_id == 1)

    def test_find_by_event_id_and_person_id(self):
        enrollments = self.enrollments.find_all()
        self.assertTrue(self.enrollments.find_by_event_id_and_person_id(1, 1) == enrollments[0])
        self.assertTrue(self.enrollments.find_by_event_id_and_person_id(2, 1) == enrollments[1])
        self.assertIsNone(self.enrollments.find_by_event_id_and_person_id(2, 2))

    def test_delete_by_event_id_and_person_id(self):
        self.assertTrue(len(self.enrollments.find_all()) == 2)
        self.enrollments.delete_by_event_id_and_person_id(2, 1)
        self.assertTrue(len(self.enrollments.find_all()) == 1)

        try:
            self.enrollments.delete_by_event_id_and_person_id(2, 1)
            self.assertRaises(KeyError, self.enrollments.delete_by_event_id_and_person_id(1, 1), "No enrollment with given ids was found")
        except KeyError:
            pass
