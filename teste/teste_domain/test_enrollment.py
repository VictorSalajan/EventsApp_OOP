from domain.entities import Enrollment
from unittest import TestCase


class TestEnrollment(TestCase):
    def setUp(self):
        self.enrollment = Enrollment(3, 2)

    def test_event_id(self):
        self.assertTrue(self.enrollment.event_id == 3, "Event id should be 3")

    def test_person_id(self):
        self.assertTrue(self.enrollment.person_id == 2, "Person id should be 2")
