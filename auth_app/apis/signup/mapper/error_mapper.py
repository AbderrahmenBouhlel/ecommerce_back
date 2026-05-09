from core.apiResponse.response import ApiResponse, ApiCode
from core.exceptions.excecptions import (
    RequestValidationException,
    ServerUnavailableException,
    InternalServerErrorException,
)
from auth_app.apis.signup.exceptions import (
    InvalidEmailException,
    WeakPasswordException,
    EmailAlreadyExistsException,
)


class SignupErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid signup request. Check required fields and data formats.",
                status=400,
            )

        if isinstance(exception, InvalidEmailException):
            return ApiResponse(
                code=ApiCode.VALIDATION_INVALID_EMAIL,
                message="Email format is invalid.",
                status=400,
            )

        if isinstance(exception, WeakPasswordException):
            return ApiResponse(
                code=ApiCode.VALIDATION_WEAK_PASSWORD,
                message="Password must be at least 8 characters long and include letters and numbers.",
                status=400,
            )

        if isinstance(exception, EmailAlreadyExistsException):
            return ApiResponse(
                code=ApiCode.AUTH_EMAIL_ALREADY_EXISTS,
                message="An account with this email already exists.",
                status=409,
            )

        if isinstance(exception, ServerUnavailableException):
            return ApiResponse(
                code=ApiCode.SYSTEM_SERVICE_UNAVAILABLE,
                message="Service temporarily unavailable.",
                status=503,
            )

        if isinstance(exception, InternalServerErrorException):
            return ApiResponse(
                code=ApiCode.SYSTEM_INTERNAL_ERROR,
                message="Internal server error.",
                status=500,
            )

        return ApiResponse(
            code=ApiCode.SYSTEM_INTERNAL_ERROR,
            message="Internal server error.",
            status=500, 
        )
       