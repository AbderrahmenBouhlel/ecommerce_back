from core.exceptions.excecptions import AppException


class ProductNotFoundException(AppException):
    def __init__(self, message: str = "The product you are trying to add a variant to does not exist.", cause: Exception = None):
        super().__init__(message, 404, cause)
