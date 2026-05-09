from core.exceptions.excecptions import AppException


class CategoryNameAlreadyExistsException(AppException):
    def __init__(self, message: str = "A category with this name already exists for this gender.", cause: Exception = None):
        super().__init__(message, 409, cause)