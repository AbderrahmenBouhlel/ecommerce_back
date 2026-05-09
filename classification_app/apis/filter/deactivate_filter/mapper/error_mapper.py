from classification_app.apis.filter.deactivate_filter.exception import FilterAlreadyInactiveException
from classification_app.errors import FilterNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class DeactivateFilterErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid request. dues to missing or invalid parameters.",
                status=400,
            )

        if isinstance(exception, FilterAlreadyInactiveException):
            return ApiResponse(
                code=ApiCode.FILTER_ALREADY_INACTIVE,
                message="Filter is already inactive.",
                status=409,
            )

        if isinstance(exception, FilterNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_NOT_FOUND,
                message="Filter not found.",
                status=404,
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