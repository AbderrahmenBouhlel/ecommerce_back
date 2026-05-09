from core.exceptions.excecptions import AppException


class CategoryInactiveException(AppException):
    def __init__(self, message: str = "Cannot assign product to an inactive category.", cause: Exception = None):
        super().__init__(message, 409, cause)