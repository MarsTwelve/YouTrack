class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class DuplicateDataException(Exception):
    def __init__(self, messsage):
        super().__init__(messsage)
