from datetime import datetime
from domain.entities import Event, Person, Enrollment
from repository.enrollments_repository import EnrollmentRepository
from repository.generic_repo import Repository


class EventFileRepository(Repository):
    def __init__(self, filename, enrollments_filename):
        super().__init__()
        self.__filename = filename
        self.__enrollments_filename = enrollments_filename
        self.__load_data()

    def __load_data(self):
        """
        Reads data from file repository and saves each transformed line to the in-memory repository
        :return:
        """
        with open(self.__filename) as f:
            for line in f:
                array = line.strip().split(',')     # line without '\n'
                event = Event(int(array[0]), datetime.strptime(array[1], "%d %m %Y"), int(array[2]), array[3])  # str -> datetime(str) when loading data
                super().save(event)

    def __write_file(self):
        """
        Writes string representation of each object from in-memory repository to a file repository, line by line
        :return:
        """
        with open(self.__filename, 'w') as f:
            for event in self.find_all():
                f.write(f'{event.id},{datetime.strftime(event.date, "%d %m %Y")},{event.time},{event.description}\n')

    def save(self, event):
        """
        Saves an Event object to in-memory repository and then appends it to file repository
        :param event: Object of type Event
        :return:
        """
        super().save(event)             # handles duplicate id error

        with open(self.__filename, 'a') as f:
            f.write(f'{event.id},{datetime.strftime(event.date, "%d %m %Y")},{event.time},{event.description}\n')

    def update(self, event):
        """
        Updates an Event object in the in-memory repository
        and then writes the updated repository to the file repository
        :param event: Object of type Event
        :return:
        """
        super().update(event)
        self.__write_file()

    def delete_by_id(self, event_id):
        """
        Deletes an event by id from both in-memory and file repositories and
        subsequently deletes enrollments associated with that event id
        :param event_id: int
        :return:
        """
        super().delete_by_id(event_id)
        self.__write_file()

        # cascade delete
        with open(self.__enrollments_filename) as f:
            lines = f.readlines()
            filtered_lines = list(filter(lambda line: int(line.split(',')[0]) != event_id, lines))

        with open(self.__enrollments_filename, 'w') as f:
            for line in filtered_lines:
                f.write(line)


class PersonFileRepository(Repository):
    def __init__(self, filename, enrollments_filename):
        super().__init__()
        self.__filename = filename
        self.__enrollments_filename = enrollments_filename
        self.__load_data()

    def __load_data(self):
        """
        Reads data from file repository and saves each transformed line to the in-memory repository
        :return:
        """
        with open(self.__filename) as f:
            for line in f:
                array = line.strip().split(',')
                person = Person(int(array[0]),array[1],array[2])
                super().save(person)

    def __write_file(self):
        """
        Writes string representation of each object from in-memory repository to a file repository, line by line
        :return:
        """
        with open(self.__filename, 'w') as f:
            for person in self.find_all():
                f.write(f'{person.id},{person.name},{person.address}\n')

    def save(self, person):
        """
        Saves a Person object to in-memory repository and then appends it to file repository
        :param person: Object of type Person
        :return:
        """
        super().save(person)

        with open(self.__filename, 'a') as f:
            f.write(f'{person.id},{person.name},{person.address}\n')

    def update(self, person):
        """
        Updates an Person object in the in-memory repository
        and then writes the updated repository to the file repository
        :param person: Object of type Person
        :return:
        """
        super().update(person)
        self.__write_file()

    def delete_by_id(self, person_id):
        """
        Deletes a person by id from both in-memory and file repositories and
        subsequently deletes enrollments associated with that person id
        :param person_id: int
        :return:
        """
        super().delete_by_id(person_id)
        self.__write_file()

        # cascade delete in enrollments file
        with open(self.__enrollments_filename) as f:
            lines = f.readlines()
            filtered_lines = list(filter(lambda line: int(line.strip().split(',')[1]) != person_id, lines))

        with open(self.__enrollments_filename, 'w') as f:
            for line in filtered_lines:
                f.write(line)


class EnrollmentFileRepository(EnrollmentRepository):
    def __init__(self, filename, event_repository, person_repository):    # these will be EventFile & PersonFile repos (passed in main)
        super().__init__(event_repository, person_repository)             # must declare repos as params consistent with parent class
        self.__filename = filename
        self.__load_data()

    def __load_data(self):
        """
        Reads data from file repository and saves each transformed line to the in-memory repository
        :return:
        """
        with open(self.__filename) as f:
            for line in f:
                array = line.strip().split(',')
                enrollment = Enrollment(int(array[0]), int(array[1]))
                super().save(enrollment)

    def __write_file(self):
        """
        Writes string representation of each object from in-memory repository to a file repository, line by line
        :return:
        """
        with open(self.__filename, 'w') as f:
            for enrollment in self.find_all():
                f.write(f'{enrollment.event_id},{enrollment.person_id}\n')

    def save(self, enrollment):
        """
        Saves an Enrollment object to in-memory repository and then appends it to file repository
        :param enrollment: Object of type Enrollment
        :return:
        """
        super().save(enrollment)

        with open(self.__filename, 'a') as f:
            f.write(f'{enrollment.event_id},{enrollment.person_id}\n')

    def delete_by_event_id_and_person_id(self, event_id, person_id):
        """
        Deletes an enrollment by event_id and person_id from both in-memory and file repositories
        :param event_id: int
        :param person_id: int
        :return:
        """
        super().delete_by_event_id_and_person_id(event_id, person_id)
        self.__write_file()
