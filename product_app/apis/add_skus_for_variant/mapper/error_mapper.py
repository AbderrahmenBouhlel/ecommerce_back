from core.apiResponse.response import ApiCode, ApiResponse
from core.exceptions.excecptions import InternalServerErrorException, RequestValidationException, ServerUnavailableException
from product_app.apis.add_skus_for_variant.exception.exception import  ProductArchivedException, DuplicateSizeInVariantException
from product_app.errors import ProductVariantNotFoundException


class AddSkusForVariantErrorMapper:
    @staticmethod
    def map(exception: Exception) -> ApiResponse:
        if isinstance(exception, RequestValidationException):
            message = exception.message if exception.message else "Invalid request."
            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=message,
                status=400,
            )

        if isinstance(exception, ProductVariantNotFoundException):
            return ApiResponse(
                code=ApiCode.RESOURCE_NOT_FOUND,
                message="The specified variant does not exist.",
                status=404,
            )

        if isinstance(exception, ProductArchivedException):
            return ApiResponse(
                code=ApiCode.PRODUCT_ARCHIVED,
                message="Cannot add SKUs to a variant belonging to an archived product.",
                status=409,
            )

        if isinstance(exception, DuplicateSizeInVariantException):
            message = exception.message if exception.message else "A SKU with the same size already exists for this variant."
            return ApiResponse(
                code=ApiCode.SKU_DUPLICATE_SIZE_IN_VARIANT,
                message=message,
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
