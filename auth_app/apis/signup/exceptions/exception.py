from core.exceptions.excecptions import AppException



class InvalidEmailException(AppException):
    def __init__(self, message: str = "Email format is invalid.", cause: Exception = None):
        super().__init__(message, 400, cause)


class WeakPasswordException(AppException):
    def __init__(self, message: str = "Password is too weak.", cause: Exception = None):
        super().__init__(message, 400, cause)


class EmailAlreadyExistsException(AppException):
    def __init__(self, message: str = "An account with this email already exists.", cause: Exception = None):
        super().__init__(message, 409, cause)