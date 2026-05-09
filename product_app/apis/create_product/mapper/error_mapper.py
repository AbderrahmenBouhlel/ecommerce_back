from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException , RequestValidationException
from product_app.errors import CategoryInactiveException, ProductCategoryNotFoundException, ProductNameAlreadyExistsException


class CreateProductErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            message = exception.message if exception.message else "Invalid product creation request."
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=message,
                status=400,
            )

        if isinstance(exception, ProductCategoryNotFoundException):
            return ApiResponse(
                code=ApiCode.CATEGORY_NOT_FOUND,
                message="The specified category does not exist.",
                status=404,
            )

        if isinstance(exception, CategoryInactiveException):
            return ApiResponse(
                code=ApiCode.CATEGORY_INACTIVE,
                message="Cannot assign product to an inactive category.",
                status=409,
            )

        if isinstance(exception, ProductNameAlreadyExistsException):
            return ApiResponse(
                code=ApiCode.PRODUCT_DUPLICATE_NAME,
                message="A product with this name already exists.",
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