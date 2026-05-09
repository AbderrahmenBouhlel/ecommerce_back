from classification_app.apis.filter_value.hard_delete_filter_value.exception import FilterValueNotFoundException
from classification_app.errors import ConfirmationRequiredException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class HardDeleteFilterValueErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid request. dues to missing or invalid parameters.",
                status=400,
            )

        if isinstance(exception, ConfirmationRequiredException):
            return ApiResponse(
                code=ApiCode.REQUEST_CONFIRMATION_REQUIRED,
                message="Deletion confirmation is required.",
                status=400,
            )

        if isinstance(exception, FilterValueNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_VALUE_NOT_FOUND,
                message="Filter value not found.",
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
