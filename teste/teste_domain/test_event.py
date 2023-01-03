from domain.entities import Event
from datetime import datetime
from unittest import TestCase


class TestEvent(TestCase):
    def setUp(self):
        self.event = Event(1, datetime(day=10, month=10, year=2020), 60, "descriere")

    def test_id(self):
        self.assertTrue(self.event.id == 1, "Event id should be 1")

    def test_date(self):
        self.assertTrue(self.event.date == datetime(day=10, month=10, year=2020), "Event date should be '10 10 2020'")

    def test_time(self):
        self.assertTrue(self.event.time == 60, "Event time should be 60")

    def test_description(self):
        self.assertTrue(self.event.description == "descriere", 'Event description should be "descriere"')
