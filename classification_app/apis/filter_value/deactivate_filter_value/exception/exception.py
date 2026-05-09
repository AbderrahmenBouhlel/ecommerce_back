from core.exceptions.excecptions import AppException




class FilterValueAlreadyInactiveException(AppException):
    def __init__(self, message: str = "Filter value is already inactive.", cause: Exception = None):
        super().__init__(message, 409, cause)