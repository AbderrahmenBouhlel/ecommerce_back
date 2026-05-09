from core.exceptions.excecptions import AppException


class CategoryFilterAlreadyEnabledException(AppException):
    def __init__(
        self,
        message: str = "This filter is already enabled for this category.",
        cause: Exception = None,
    ):
        super().__init__(message, 409, cause)