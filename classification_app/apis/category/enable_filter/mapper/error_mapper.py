from classification_app.apis.category.enable_filter.exception import CategoryFilterAlreadyEnabledException
from classification_app.errors import CategoryNotFoundException, FilterNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
)


class EnableCategoryFilterErrorMapper:
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
                message="The specified category does not exist.",
                status=404,
            )

        if isinstance(exception, FilterNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_NOT_FOUND,
                message="The specified filter does not exist.",
                status=404,
            )

        if isinstance(exception, CategoryFilterAlreadyEnabledException):
            return ApiResponse(
                code=ApiCode.CATEGORY_FILTER_ALREADY_ENABLED,
                message="This filter is already enabled for this category.",
                status=409,
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