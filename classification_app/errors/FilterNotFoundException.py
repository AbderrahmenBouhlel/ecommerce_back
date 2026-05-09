



from core.exceptions.excecptions import AppException


class FilterNotFoundException(AppException):
    def __init__(self, message: str = "Filter not found.", cause: Exception = None):
        super().__init__(message, 404, cause)
    