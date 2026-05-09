from core.exceptions.excecptions import AppException


class FilterAlreadyInactiveException(AppException):
    def __init__(self, message: str = "Filter is already inactive.", cause: Exception = None):
        super().__init__(message, 409, cause)