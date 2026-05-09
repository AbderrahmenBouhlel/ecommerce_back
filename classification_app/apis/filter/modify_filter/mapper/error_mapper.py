from classification_app.apis.filter.modify_filter.exception import FilterAlreadyExistsException
from classification_app.errors import FilterNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class ModifyFilterErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid request. dues to missing or invalid parameters.",
                status=400,
            )

        if isinstance(exception, FilterNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_NOT_FOUND,
                message="Filter not found.",
                status=404,
            )

        if isinstance(exception, FilterAlreadyExistsException):
            return ApiResponse(
                code=ApiCode.FILTER_NAME_ALREADY_EXISTS,
                message="A filter with this name already exists.",
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