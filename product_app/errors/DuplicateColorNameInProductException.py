
from core.exceptions.excecptions import AppException


class DuplicateColorNameInProductException(AppException):
    def __init__(self, message: str = "A variant with this color name already exists for this product.", cause: Exception = None):
        super().__init__(message, 409, cause)
