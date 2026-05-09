from core.exceptions.excecptions import AppException


class ProductVariantNotFoundException(AppException):
    def __init__(self, message: str = "The product variant you are trying to access does not exist.", cause: Exception = None):
        super().__init__(message, 404, cause)
