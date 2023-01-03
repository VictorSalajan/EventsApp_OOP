from domain.entities import Person
from unittest import TestCase


class TestPerson(TestCase):
    def setUp(self):
        self.person = Person(1, "Ana", "adresa")

    def test_id(self):
        self.assertTrue(self.person.id == 1, "Person id should be 1")

    def test_name(self):
        self.assertTrue(self.person.name == "Ana", "Person's name should be 'Ana'")

    def test_address(self):
        self.assertTrue(self.person.address == "adresa", "Person's address should be 'adresa'")
