from classification_app.apis.category.deactiavte_category.exception import CategoryAlreadyInactiveException
from classification_app.errors import CategoryNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import (
    InternalServerErrorException,
    RequestValidationException,
    ServerUnavailableException,
)


class DeactivateCategoryErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message="Invalid request. dues to missing or invalid parameters.",
                status=400,
            )

        if isinstance(exception, CategoryAlreadyInactiveException):
            return ApiResponse(
                code=ApiCode.CATEGORY_ALREADY_INACTIVE,
                message="Category is already inactive.",
                status=409,
            )

        if isinstance(exception, CategoryNotFoundException):
            return ApiResponse(
                code=ApiCode.CATEGORY_NOT_FOUND,
                message="Category not found.",
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