from core.exceptions.excecptions import AppException


class AccountDisabledException(AppException):
    def __init__(self ,message: str, cause: Exception = None):
        # We pass 403 here because it's a Forbidden error
        super().__init__(message, 403, cause)
        