from domain.exceptions.validation_error import ValidationError
from domain.entities import Event
from repository.generic_repo import Repository


class EventValidator:
    @staticmethod
    def validate_event(event: Event, event_repository: Repository):
        errors = []
        if event.time <= 0:
            errors.append("Event duration must be a positive integer")
        if event.description == '':
            errors.append("Event description cannot be empty string")
        events = event_repository.find_all()
        descriptions = [event.description for event in events]
        if event.description in descriptions:
            errors.append("Event descriptions should be unique")
        if errors:
            raise ValidationError(errors)
