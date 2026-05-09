from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import InternalServerErrorException, RequestValidationException, ServerUnavailableException
from product_app.errors import ProductNotFoundException
from classification_app.errors import FilterValueNotFoundException
from product_app.apis.add_filter_values_for_product.exception.exception import FilterValueNotAllowedException


class AddFilterValuesForProductErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            message = exception.message if exception.message else "Invalid request."
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=message,
                status=400,
            )

        if isinstance(exception, ProductNotFoundException):
            return ApiResponse(
                code=ApiCode.PRODUCT_NOT_FOUND,
                message="The specified product does not exist.",
                status=404,
            )

        if isinstance(exception, FilterValueNotFoundException):
            return ApiResponse(
                code=ApiCode.FILTER_VALUE_NOT_FOUND,
                message="One or more filter values do not exist.",
                status=404,
            )

        if isinstance(exception, FilterValueNotAllowedException):
            return ApiResponse(
                code=ApiCode.FILTER_VALUE_NOT_ALLOWED_FOR_CATEGORY,
                message="One or more filter values are not allowed for this product category.",
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
