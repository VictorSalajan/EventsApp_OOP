from repository.persons_repository import PersonRepository
from domain.entities import Person
from unittest import TestCase


class TestPerson(TestCase):
    def setUp(self):
        self.person_repository = PersonRepository()
        self.person1 = Person(1, "Ana Maria", "Cluj")
        self.person2 = Person(2, "Mihai Ionescu", "Bucuresti")
        self.person3 = Person(3, "Joe Biden", "Washington")

        self.person_repository.save(self.person1)
        self.person_repository.save(self.person3)

    def test_save(self):
        self.person_repository.save(self.person2)

        person = self.person_repository.find_all()[2]
        self.assertTrue(person.id == 2, "Person's id should be 2")
        self.assertTrue(person.name == "Mihai Ionescu", "Person's name should be Mihai Ionescu")
        self.assertTrue(person.address == "Bucuresti", "Person's address should be 'Bucuresti'")

        try:
            self.person_repository.save(self.person2)
            self.assertRaises(KeyError, self.person_repository.save(self.person2), "Duplicate id")
        except KeyError:
            pass

    def test_update(self):
        person = Person(1, "George Constantinescu", "Iasi")
        self.person_repository.update(person)

        person = self.person_repository.find_all()[0]
        self.assertTrue(person.id == 1, "Person's id should be 1")
        self.assertTrue(person.name == "George Constantinescu", "Person's name should be George Constantinescu")
        self.assertTrue(person.address == "Iasi", "Person's address should be Iasi")

        try:
            person = Person(2, "Ana", "Cluj")
            self.person_repository.update(person)
            self.assertRaises(KeyError, self.person_repository.update(person), "Id does not exist")
        except KeyError:
            pass

    def test_find_by_id(self):
        self.assertIsNotNone(self.person_repository.find_by_id(1))
        self.assertIsNotNone(self.person_repository.find_by_id(3))
        self.assertIsNone(self.person_repository.find_by_id(2))

    def test_find_all(self):
        self.assertTrue(len(self.person_repository.find_all()) == 2)
        self.assertTrue(self.person_repository.find_all()[0].id == 1)
        self.assertTrue(self.person_repository.find_all()[1].id == 3)

    def test_delete_by_id(self):
        self.assertTrue(len(self.person_repository.find_all()) == 2)
        self.person_repository.delete_by_id(1)
        self.assertTrue(len(self.person_repository.find_all()) == 1)
        self.assertTrue(self.person_repository.find_all()[0].id == 3)

        try:
            self.person_repository.delete_by_id(1)
            self.assertRaises(KeyError, self.person_repository.delete_by_id(1), "Id does not exist")
        except KeyError:
            pass
