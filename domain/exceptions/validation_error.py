

class ValidationError(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'ValidationError: {self.__message}'
