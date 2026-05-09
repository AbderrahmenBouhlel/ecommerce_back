from core.exceptions.excecptions import AppException


class CategoryAlreadyInactiveException(AppException):
    def __init__(self, message: str = "Category is already inactive.", cause: Exception = None):
        super().__init__(message, 409, cause)