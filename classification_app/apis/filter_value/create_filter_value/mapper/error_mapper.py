from classification_app.apis.filter_value.create_filter_value.exception import ( FilterValueAlreadyExistsException)
from classification_app.errors import FilterNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class CreateFilterValueErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid filter value request.",
                status=400,
            )

        if isinstance(exception, FilterNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_NOT_FOUND,
                message="Filter not found.",
                status=404,
            )

        if isinstance(exception, FilterValueAlreadyExistsException):
            return ApiResponse(
                code=ApiCode.FILTER_VALUE_ALREADY_EXISTS,
                message="This value already exists for the filter.",
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
