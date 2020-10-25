class CustomException(Exception):

    def __init__(self, pointer, code, message=None):
        self.response = {"pointer": pointer, "message": message}
        self.code = code


class NotFoundException(CustomException):
    def __init__(self, pointer, message=None):
        super().__init__(pointer, 404, message)


class ConflictException(CustomException):
    def __init__(self, pointer, message=None):
        super().__init__(pointer, 409, message)
