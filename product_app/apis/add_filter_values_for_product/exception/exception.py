from core.exceptions.excecptions import AppException


class FilterValueNotAllowedException(AppException):
    def __init__(self, message: str = "One or more filter values are not allowed for this product category.", cause: Exception = None):
        super().__init__(message=message, cause=cause)


__all__ = ["FilterValueNotAllowedException"]
