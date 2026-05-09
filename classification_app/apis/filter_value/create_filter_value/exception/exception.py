from core.exceptions.excecptions import AppException




class FilterValueAlreadyExistsException(AppException):
    def __init__(self, message: str = "This value already exists for the filter.", cause: Exception = None):
        super().__init__(message, 409, cause)
