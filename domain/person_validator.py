from domain.entities import Person
from domain.exceptions.validation_error import ValidationError


class PersonValidator:
    @staticmethod
    def validate_person(person: Person):
        errors = []
        if person.name == '':
            errors.append("A person's name cannot be an empty string")
        if len(person.name) > 30:
            errors.append("A person's name cannot be longer than 30 characters")
        if errors:
            raise ValidationError(errors)
