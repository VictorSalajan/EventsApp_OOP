from repository.events_repository import EventRepository
from domain.entities import Event
from datetime import datetime
from unittest import TestCase

class TestEventRepository(TestCase):
    def setUp(self):
        self.event_repository = EventRepository()
        date = datetime(day=2, month=10, year=2020)
        self.event1 = Event(1, date, 60, "descriere")
        self.event2 = Event(2, date, 30, "conferinta")
        self.event3 = Event(3, date, 90, "prelegere")

        self.event_repository.save(self.event1)
        self.event_repository.save(self.event3)

    def test_save(self):
        self.event_repository.save(self.event2)

        event = self.event_repository.find_all()[2]
        self.assertTrue(event.id == 2, "Event id should be 2")
        self.assertTrue(event.date == datetime(day=2, month=10, year=2020), "Event date should be '2 10 2020'")
        self.assertTrue(event.time == 30, "Event time should be 30")
        self.assertTrue(event.description == "conferinta", "Event description should be 'conferinta'")

        try:
            self.event_repository.save(self.event2)
            self.assertRaises(KeyError, self.event_repository.save(self.event2), "Duplicate id")
        except KeyError:
            pass

    def test_update(self):
        date = datetime(day=12, month=1, year=2022)

        self.event_repository.update(Event(1, date, 100, 'workshop informatica'))
        event = self.event_repository.find_all()[0]

        self.assertTrue(event.id == 1, "Event id should be 1")
        self.assertTrue(event.date == date, "Event date should be '12 1 2022'")
        self.assertTrue(event.time == 100, "Event date should be 100")
        self.assertTrue(event.description == 'workshop informatica', "Event description should be 'workshop informatica'")

        try:
            event = Event(2, date, 10, "descriere noua")
            self.event_repository.update(event)
            self.assertRaises(KeyError, self.event_repository.update(event), "Id does not exist")
        except KeyError:
            pass

    def test_find_all(self):
        self.event_repository.save(self.event2)
        self.assertTrue(len(self.event_repository.find_all()) == 3)
        self.assertTrue(self.event_repository.find_all()[0].id == 1)
        self.assertTrue(self.event_repository.find_all()[1].id == 3)
        self.assertTrue(self.event_repository.find_all()[2].id == 2)

    def test_find_by_id(self):
        self.assertIsNotNone(self.event_repository.find_by_id(1))
        self.assertIsNotNone(self.event_repository.find_by_id(3))
        self.assertIsNone(self.event_repository.find_by_id(2))

    def test_delete_by_id(self):
        self.assertTrue(len(self.event_repository.find_all()) == 2)
        self.event_repository.delete_by_id(3)
        self.assertTrue(len(self.event_repository.find_all()) == 1)
        self.assertTrue(self.event_repository.find_all()[0].id == 1)

        try:
            self.event_repository.delete_by_id(3)
            self.assertRaises(KeyError, self.event_repository.delete_by_id(3), "Id does not exist")
        except KeyError:
            pass
