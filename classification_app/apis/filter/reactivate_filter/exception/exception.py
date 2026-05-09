from core.exceptions.excecptions import AppException


class FilterAlreadyActiveException(AppException):
    def __init__(self, message: str = "Filter is already active.", cause: Exception = None):
        super().__init__(message, 409, cause)