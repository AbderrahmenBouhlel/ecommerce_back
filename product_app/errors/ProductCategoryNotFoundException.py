from core.exceptions.excecptions import AppException


class ProductCategoryNotFoundException(AppException):
    def __init__(self, message: str = "The specified category does not exist.", cause: Exception = None):
        super().__init__(message, 404, cause)