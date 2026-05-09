


from core.exceptions.excecptions import AppException


class DuplicateColorNameInProductException(AppException):
    def __init__(self, message: str = "A variant with this color name already exists for this product.", cause: Exception = None):
        super().__init__(message, 409, cause)



class DuplicateColorNameInProductException(AppException):
    def __init__(
        self,
        message: str = "A variant with this color name already exists for this product.",
        cause: Exception = None
    ):
        super().__init__(message, 409, cause)


class UnsupportedImageContentTypeException(AppException):
    def __init__(
        self,
        message: str = "One or more uploaded images have an unsupported content type.",
        cause: Exception = None
    ):
        super().__init__(message, 400, cause)


class ImagesSizeLimitExceededException(AppException):
    def __init__(
        self,
        message: str = "Total uploaded images size exceeds the allowed limit.",
        cause: Exception = None
    ):
        super().__init__(message, 413, cause)