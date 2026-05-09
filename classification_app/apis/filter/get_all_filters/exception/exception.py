from core.exceptions.excecptions import AppException


class GetAllFiltersException(AppException):
    def __init__(self, message: str = "Failed to retrieve filters.", cause: Exception = None):
        super().__init__(message, 500, cause)
