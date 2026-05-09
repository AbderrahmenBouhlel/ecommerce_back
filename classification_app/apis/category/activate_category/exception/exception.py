from core.exceptions.excecptions import AppException


class CategoryAlreadyActiveException(AppException):
    def __init__(self, message: str = "Category is already active.", cause: Exception = None):
        super().__init__(message, 409, cause)