from core.exceptions.excecptions import AppException


class CategoryAlreadyExistsException(AppException):
    def __init__(
        self,
        message: str = "A category with this name and gender combination already exists.",
        cause: Exception = None,
    ):
        super().__init__(message, 409, cause)