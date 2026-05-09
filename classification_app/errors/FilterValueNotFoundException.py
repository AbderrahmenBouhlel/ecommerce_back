from core.exceptions import AppException



class FilterValueNotFoundException(AppException):
    def __init__(self, message: str = "Filter value not found.", cause: Exception = None):
        super().__init__(message, 404, cause)

