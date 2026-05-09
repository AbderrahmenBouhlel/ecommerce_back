from core.exceptions.excecptions import AppException


class FilterNameAlreadyExistsException(AppException):
    def __init__(self, message: str = "A filter with this name already exists.", cause: Exception = None):
        super().__init__(message, 409, cause)
        