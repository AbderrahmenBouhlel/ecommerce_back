from core.exceptions.excecptions import AppException


class CategoryFilterNotAssociatedException(AppException):
    def __init__(
        self,
        message: str = "This filter is not associated with the category.",
        cause: Exception = None,
    ):
        super().__init__(message, 409, cause)