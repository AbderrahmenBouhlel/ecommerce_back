

from auth_app.apis.login.exception import AccountDisabledException
from core.apiResponse.response import ApiResponse , ApiCode
from core.exceptions.excecptions import (
    RequestValidationException,
    InvalidCredentialsException,
    InternalServerErrorException,
    ServerUnavailableException,
)



class LoginErrorMapper:
    
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        """
        Translates any exception into ApiResponse based on Login API's specific JSON contract.
        """
        
        # 1. Handle Request Validation (400)
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=exception.message,
                status=400
            )
            
        # 2. Handle Invalid Credentials (401)
        if isinstance(exception, InvalidCredentialsException):
            return ApiResponse(
                code=ApiCode.AUTH_INVALID_CREDENTIALS,
                message="Invalid credentials.",
                status=401 
            )
            
        # 3. Handle Service/DB Unavailable (503)
        if isinstance(exception, ServerUnavailableException):
            return ApiResponse(
                code=ApiCode.SYSTEM_SERVICE_UNAVAILABLE,
                message="Server is currently unavailable.",
                status= 503
            )
            
        # 4. Handle Known Internal Errors (500)
        if isinstance(exception, InternalServerErrorException):
            return ApiResponse(
                code=ApiCode.SYSTEM_INTERNAL_ERROR,
                message="Internal server error.",
                status=500
            )
            
        # 5. Handle Account Inactive (403)
        if isinstance(exception, AccountDisabledException):
            return ApiResponse(
                code=ApiCode.AUTH_USER_INACTIVE,
                message="Account is deactivated.",
                status=403
            )
            
        return ApiResponse(
            code=ApiCode.SYSTEM_INTERNAL_ERROR,
            message="Internal server error.",
            status=500
        )