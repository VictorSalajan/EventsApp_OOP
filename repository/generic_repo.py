

class Repository:                             # instead of separate Event and Person repositories
    def __init__(self):
        self.__entities = {}

    def save(self, entity):
        """
        Adauga o persoana in dictionarul de entitati
        :param entity: object of type Entity
        :return:
        """
        if self.find_by_id(entity.id):
            raise KeyError("Duplicate id")
        self.__entities[entity.id] = entity

    def update(self, entity):
        """
        Modifica o entitate dupa id
        :param entity: object of type Entity
        :return:
        """
        if self.find_by_id(entity.id) is None:
            raise KeyError("Id not found")
        self.__entities[entity.id] = entity

    def find_all(self):
        """
        Returneaza o lista de entitati
        :return: list of objects of type Entity
        """
        return list(self.__entities.values())

    def find_by_id(self, id):
        """
        Returneaza entitatea cu un id dat
        :param id: int
        :return: object of type Entity or None
        """
        return self.__entities.get(id, None)

    def delete_by_id(self, id):
        """
        Sterge o entitate dupa id
        :param id: int
        :return:
        """
        if self.find_by_id(id) is None:
            raise KeyError("Id not found")
        self.__entities.pop(id)
