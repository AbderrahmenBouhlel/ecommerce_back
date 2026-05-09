from core.exceptions.excecptions import AppException

class FilterValueAlreadyActiveException(AppException):
    def __init__(self, message: str = "Filter value is already active.", cause: Exception = None):
        super().__init__(message, 409, cause)