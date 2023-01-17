from domain.event_validator import EventValidator
from domain.person_validator import PersonValidator
from repository.file_repository import EventFileRepository, PersonFileRepository, EnrollmentFileRepository
from repository.generic_repo import Repository
from ui.console import Console
from repository.enrollments_repository import EnrollmentRepository
from service.events_service import EventService
from service.persons_service import PersonService
from service.enrollments_service import EnrollmentService


def choose_repository():
    while True:
        print("1. Use in-memory repository")
        print("2. Use file repository")
        print("x. Exit")
        option = input("Choose the repository: ")
        if option == "1":
            event_repository = Repository()
            person_repository = Repository()
            enrollment_repository = EnrollmentRepository(event_repository, person_repository)
            return event_repository, person_repository, enrollment_repository
        elif option == "2":
            event_repository = EventFileRepository('data/events', 'data/enrollments')
            person_repository = PersonFileRepository('data/persons', 'data/enrollments')
            enrollment_repository = EnrollmentFileRepository('data/enrollments', event_repository, person_repository)
            return event_repository, person_repository, enrollment_repository
        elif option == "x":
            return
        else:
            print('Wrong option! Try again.')


def main():
    repos = choose_repository()     # avoiding unpacking a NoneType object (option 'x')
    if not repos:
        return
    event_repository, person_repository, enrollment_repository = repos

    event_validator = EventValidator()
    person_validator = PersonValidator()

    event_service = EventService(event_repository, enrollment_repository, event_validator)       # enrollment is used for cascade delete
    person_service = PersonService(person_repository, enrollment_repository, person_validator)

    enrollment_service = EnrollmentService(enrollment_repository, event_repository, person_repository)

    console = Console(event_service, person_service, enrollment_service)

    console.menu()


main()
