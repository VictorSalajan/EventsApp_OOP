from repository.generic_repo import Repository
from unittest import TestCase
from unittest.mock import Mock


class TestRepository(TestCase):
    def setUp(self):
        self.mock1 = Mock()
        self.mock2 = Mock()
        self.mock1.id = 1
        self.mock2.id = 2
        self.mock1.attr = 'val 1'
        self.mock2.attr = 'val 2'
        self.repository = Repository()
        self.repository.save(self.mock1)
        self.repository.save(self.mock2)

    def test_save(self):
        try:
            self.repository.save(self.mock2)
            self.assertRaises(KeyError, self.repository.save(self.mock2), "Duplicate id")
        except KeyError:
            pass

    def test_update(self):
        new_mock1 = Mock()
        new_mock1.id = 1
        new_mock1.attr = 'new value'
        self.repository.update(new_mock1)
        self.assertTrue(self.repository.find_all()[0] == new_mock1)

        try:
            new_mock2 = Mock()
            new_mock2.id = 3
            self.repository.update(new_mock2)
            self.assertRaises(KeyError, self.repository.update(new_mock2), "Id does not exist")
        except KeyError:
            pass

    def test_find_by_id(self):
        self.assertTrue(self.repository.find_by_id(1) == self.mock1)
        self.assertTrue(self.repository.find_by_id(3) is None)

    def test_find_all(self):
        objects = self.repository.find_all()
        self.assertTrue(objects[0] == self.mock1)
        self.assertTrue(objects[1] == self.mock2)

    def test_delete_by_id(self):
        self.repository.delete_by_id(1)
        self.assertTrue(len(self.repository.find_all()) == 1)
        self.assertTrue(self.repository.find_all()[0] == self.mock2)

        try:
            self.repository.delete_by_id(1)
            self.assertRaises(KeyError, self.repository.delete_by_id(1), "Id does not exist")
        except KeyError:
            pass
