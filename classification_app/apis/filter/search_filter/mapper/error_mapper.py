from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException, RequestValidationException


class SearchFilterErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid filter search request.",
                status=400,
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