from classification_app.apis.category.disable_filter.exception import CategoryFilterNotAssociatedException
from classification_app.errors import CategoryNotFoundException, FilterNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class DisableCategoryFilterErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid request parameters.",
                status=400,
            )

        if isinstance(exception, CategoryNotFoundException):
            return ApiResponse(
                code=ApiCode.CATEGORY_NOT_FOUND,
                message="Category not found.",
                status=404,
            )

        if isinstance(exception, FilterNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_NOT_FOUND,
                message="Filter not found.",
                status=404,
            )

        if isinstance(exception, CategoryFilterNotAssociatedException):
            return ApiResponse(
                code=ApiCode.CATEGORY_FILTER_NOT_ASSOCIATED,
                message="This filter is not associated with the category.",
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