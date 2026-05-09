



from core.exceptions.excecptions import AppException


class ConfirmationRequiredException(AppException):
    def __init__(self, message: str = "Deletion confirmation is required.", cause: Exception = None):
        super().__init__(message, 400, cause)

    