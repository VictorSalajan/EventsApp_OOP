from repository.file_repository import EventFileRepository, PersonFileRepository, EnrollmentFileRepository
from ui.console import Console
from repository.events_repository import EventRepository
from repository.persons_repository import PersonRepository
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
            event_repository = EventRepository()
            person_repository = PersonRepository()
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
    event_repository, person_repository, enrollment_repository = choose_repository()

    event_service = EventService(event_repository, enrollment_repository)       # enrollment is used for cascade delete
    person_service = PersonService(person_repository, enrollment_repository)

    enrollment_service = EnrollmentService(enrollment_repository, event_repository, person_repository)

    console = Console(event_service, person_service, enrollment_service)

    console.menu()

main()
