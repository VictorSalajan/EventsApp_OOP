from domain.exceptions.duplicate_error import DuplicateError
from domain.exceptions.validation_error import ValidationError
from service.events_service import EventService
from service.persons_service import PersonService
from service.enrollments_service import EnrollmentService
from datetime import datetime


class Console:
    def __init__(self, event: EventService, person: PersonService, enrollment: EnrollmentService):
        self.__event = event
        self.__person = person
        self.__enrollment = enrollment

    def add_event(self):
        try:
            event_id = int(input("Dati id-ul evenimentului: "))
            date = input("Dati data evenimentului, 'zi luna an': ")
            date = datetime.strptime(date, "%d %m %Y")
            time = int(input("Dati durata evenimentului: "))
            description = input("Dati descrierea evenimentului: ")
            self.__event.save(event_id, date, time, description)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)
        except ValidationError as ex:
            print(ex)
        except DuplicateError as ex:
            print(ex)

    def update_event(self):
        try:
            event_id = int(input("Dati id-ul evenimentului de modificat: "))
            date = input("Dati data noua a evenimentului: ")
            date = datetime.strptime(date, "%d %m %Y")
            time = int(input("Dati durata noua a evenimentului: "))
            description = input("Dati descrierea noua a evenimentului:")
            self.__event.update(event_id, date, time, description)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)
        except ValidationError as ex:
            print(ex)

    def delete_event_by_id(self):
        try:
            event_id = int(input("Dati id-ul evenimentului de sters: "))
            self.__event.delete_by_id(event_id)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)

    def display_events(self):
        self.print_collection(self.__event.find_all())

    def find_events_by_words_in_description(self):
        words = input("Dati cuvintele cautate in descriere: ")
        self.print_collection(self.__event.find_all_by_words_in_description(words))

    def add_person(self):
        try:
            person_id = int(input("Dati id-ul persoanei: "))
            name = input("Dati numele persoanei: ")
            address = input("Dati adresa persoanei: ")
            self.__person.save(person_id, name, address)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)
        except ValidationError as ex:
            print(ex)
        except DuplicateError as ex:
            print(ex)

    def update_person(self):
        try:
            person_id = int(input("Dati id-ul persoanei de modificat: "))
            name = input("Dati noul nume al persoanei: ")
            address = input("Dati noua adresa a persoanei: ")
            self.__person.update(person_id, name, address)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)
        except ValidationError as ex:
            print(ex)

    def delete_person_by_id(self):
        try:
            person_id = int(input("Dati id-ul persoanei de sters: "))
            self.__person.delete_by_id(person_id)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)

    def display_persons(self):
        self.print_collection(self.__person.find_all())

    def find_persons_by_string_in_name(self):
        string = input("Dati string-ul dupa care cautati persoane: ")
        self.print_collection(self.__person.find_all_by_string_in_name(string))

    def add_enrollment(self):
        try:
            event_id = int(input("Dati id-ul evenimentului de inscris: "))
            person_id = int(input("Dati id-ul persoanei de inscris: "))
            self.__enrollment.save(event_id, person_id)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)
        except DuplicateError as ex:
            print(ex)

    def update_enrollment(self):
        try:
            event_id = int(input("Dati noul id al evenimentului: "))
            person_id = int(input("Dati noul id al persoanei: "))
            self.__enrollment.save(event_id, person_id)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)

    def delete_by_event_id_and_person_id(self):
        try:
            event_id = int(input("Dati id-ul al evenimentului de sters: "))
            person_id = int(input("Dati id-ul al persoanei de sters: "))
            self.__enrollment.delete_by_event_id_and_person_id(event_id, person_id)
        except ValueError as ex:
            print(ex)
        except KeyError as ex:
            print(ex)

    def display_enrollments(self):
        self.print_collection(self.__enrollment.find_all())

    def display_events_by_person(self):
        try:
            person_id = int(input("Dati id-ul persoanei cautate: "))
            self.print_collection(self.__enrollment.events_by_person(person_id))
        except ValueError as ex:
            print(ex)

    def display_events_by_person_ordered_by_description(self):
        try:
            person_id = int(input("Dati id-ul persoanei cautate: "))
            self.print_collection(self.__enrollment.events_by_person_ordered_by_description(person_id))
        except ValueError as ex:
            print(ex)

    def display_events_by_person_ordered_by_date(self):
        try:
            person_id = int(input("Dati id-ul persoanei cautate: "))
            self.print_collection(self.__enrollment.events_by_person_ordered_by_date(person_id))
        except ValueError as ex:
            print(ex)

    def display_persons_enrolled_in_most_events(self):
        self.print_collection(self.__enrollment.persons_enrolled_in_most_events())

    def display_events_with_most_participants(self):
        self.print_collection(self.__enrollment.events_with_most_participants(0.2))

    @staticmethod
    def print_collection(collection):
        for elem in collection:
            print(elem)

    @staticmethod
    def print_menu():
        print("1. Adauga eveniment", "4. Adauga persoana".rjust(34))
        print("2. Modifica eveniment", "5. Modifica persoana".rjust(34))
        print("3. Sterge eveniment", "6. Sterge persoana".rjust(34))
        print("e. Afiseaza toate evenimentele", "p. Afiseaza toate persoanele".rjust(33))
        print("\n7. Adauga inscriere", "9. Cauta persoane dupa string in nume".rjust(53))
        print("8. Sterge inscriere", "10. Cauta evenimente dupa cuvinte in descriere".rjust(62))
        print("i. Afiseaza toate inscrierile", "11. Afiseaza evenimentele unei persoana".rjust(45))
        print("12. Afiseaza evenimentele unei persoane, ordonate dupa descriere".rjust(100))
        print("13. Afiseaza evenimentele unei persoane, ordonate dupa data".rjust(95))
        print("14. Afiseaza persoanele participante la cele mai multe evenimente".rjust(101))
        print("15. Afiseaza primele 20% evenimente cu cei mai multi participanti".rjust(101))
        print("x. Iesire")

    def menu(self):
        while True:
            self.print_menu()
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.add_event()
            elif optiune == "2":
                self.update_event()
            elif optiune == "3":
                self.delete_event_by_id()
            elif optiune == "e":
                self.display_events()
            elif optiune == "4":
                self.add_person()
            elif optiune == "5":
                self.update_person()
            elif optiune == "6":
                self.delete_person_by_id()
            elif optiune == "p":
                self.display_persons()
            elif optiune == "7":
                self.add_enrollment()
            elif optiune == "8":
                self.delete_by_event_id_and_person_id()
            elif optiune == "9":
                self.find_persons_by_string_in_name()
            elif optiune == "10":
                self.find_events_by_words_in_description()
            elif optiune == "11":
                self.display_events_by_person()
            elif optiune == "12":
                self.display_events_by_person_ordered_by_description()
            elif optiune == "13":
                self.display_events_by_person_ordered_by_date()
            elif optiune == '14':
                self.display_persons_enrolled_in_most_events()
            elif optiune == "15":
                self.display_events_with_most_participants()
            elif optiune == "i":
                self.display_enrollments()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita. Reincercati!")
