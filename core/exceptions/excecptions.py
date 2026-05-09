class AppException(Exception):
    def __init__(
                self, 
                message: str, 
                status_code: int , 
                cause: Exception = None  # Add this for observability
            ):
        super().__init__(message) 
        self.status_code = status_code
        self.message = message
        self.cause = cause  # Store the original exception for debugging/logging purposes
        
        
        
# unauthenticated 401
class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Invalid credentials." , cause: Exception = None):
        super().__init__(message, 401, cause)
        
# bad request 400  
class RequestValidationException(AppException):
    def __init__(self, message: str = "Invalid request.", cause: Exception = None):
        super().__init__(message, 400, cause)
        
# internal server error 500  
class InternalServerErrorException(AppException):
    def __init__(self, message: str = "Internal server error.", cause: Exception = None):
        super().__init__(message, 500, cause)

class ServerUnavailableException(AppException):
    def __init__(self, message: str = "Server is currently unavailable.", cause: Exception = None):
        super().__init__(message, 503, cause)
        