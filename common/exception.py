class ErrorException(Exception):
    def __init__(self, msg, code):
        self.Error = msg
        self.code = code


class NotExist(ErrorException):
    pass


class AlreadyExist(ErrorException):
    pass


class EmptyError(ErrorException):
    pass


class ServerError(ErrorException):
    pass

class PasswordMissmatched(ErrorException):
    pass