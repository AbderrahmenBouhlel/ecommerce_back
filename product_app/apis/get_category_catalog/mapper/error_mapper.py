from classification_app.errors import CategoryNotFoundException
from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import InternalServerErrorException, RequestValidationException, ServerUnavailableException
from product_app.errors import CategoryInactiveException


class GetCategoryCatalogErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            message = exception.message if exception.message else "Invalid request parameters."
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=message,
                status=400,
            )

        if isinstance(exception, CategoryNotFoundException):
            return ApiResponse(
                code=ApiCode.CATEGORY_NOT_FOUND,
                message="The specified category does not exist.",
                status=404,
            )

        if isinstance(exception, CategoryInactiveException):
            return ApiResponse(
                code=ApiCode.CATEGORY_INACTIVE,
                message="The specified category is inactive.",
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
