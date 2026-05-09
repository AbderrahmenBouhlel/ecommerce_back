from core.exceptions.excecptions import AppException


class CategoryNotFoundException(AppException):
    def __init__(self, message: str = "Category not found.", cause: Exception = None):
        super().__init__(message, 404, cause)