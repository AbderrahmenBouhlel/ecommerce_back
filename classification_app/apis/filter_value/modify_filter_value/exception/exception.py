from core.exceptions.excecptions import AppException


class FilterValueAlreadyExistsException(AppException):
    def __init__(self, message: str = "A filter value with this name already exists for the filter.", cause: Exception = None):
        super().__init__(message, 409, cause)