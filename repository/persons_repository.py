

class PersonRepository:
    def __init__(self):
        self.__persons = {}

    def save(self, person):
        """
        Adauga o persoana in dictionarul de persoane
        :param person: object of type Person
        :return:
        """
        if self.find_by_id(person.id):
            raise KeyError("Duplicate id")
        self.__persons[person.id] = person

    def update(self, person):
        """
        Modifica o persoana dupa id
        :param person: object of type Person
        :return:
        """
        if self.find_by_id(person.id) is None:
            raise KeyError("Id does not exist")
        self.__persons[person.id] = person

    def find_all(self):
        """
        Returneaza o lista de persoane
        :return: list of objects of type Person
        """
        return list(self.__persons.values())

    def find_by_id(self, person_id):
        """
        Returneaza persoana cu un id dat
        :param person_id: int
        :return: object of type Person or None
        """
        return self.__persons.get(person_id, None)

    def delete_by_id(self, person_id):
        """
        Sterge o persoana dupa id
        :param person_id: int
        :return:
        """
        if self.find_by_id(person_id) is None:
            raise KeyError("Id does not exist")
        self.__persons.pop(person_id)
