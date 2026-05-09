from core.exceptions.excecptions import AppException


class ProductArchivedException(AppException):
    def __init__(self, message: str = "Cannot add SKUs to a variant belonging to an archived product.", cause: Exception = None):
        super().__init__(message, 409, cause)


class DuplicateSizeInVariantException(AppException):
    def __init__(self, message: str = "This variant already has an SKU with this size.", cause: Exception = None):
        super().__init__(message, 409, cause)
