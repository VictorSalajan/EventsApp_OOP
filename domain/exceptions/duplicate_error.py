

class DuplicateError(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'DuplicateError: {self.__message}'
