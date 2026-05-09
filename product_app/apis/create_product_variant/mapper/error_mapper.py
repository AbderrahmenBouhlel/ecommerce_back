from core.apiResponse.response import ApiCode, ApiResponse

from core.exceptions.excecptions import (
    InternalServerErrorException,
    ServerUnavailableException,
    RequestValidationException,
)

from product_app.errors import ProductNotFoundException

from product_app.apis.create_product_variant.exception import (
    DuplicateColorNameInProductException,
    UnsupportedImageContentTypeException,
    ImagesSizeLimitExceededException,
)


class CreateProductVariantErrorMapper:

    @staticmethod
    def map(exception: Exception) -> ApiResponse:

        if isinstance(exception, RequestValidationException):
            message = (
                exception.message
                if exception.message
                else "Invalid product variant creation request."
            )

            return ApiResponse(
                code=ApiCode.REQUEST_INVALID,
                message=message,
                status=400,
            )

        if isinstance(exception, ProductNotFoundException):
            return ApiResponse(
                code=ApiCode.PRODUCT_NOT_FOUND,
                message="The product you are trying to add a variant to does not exist.",
                status=404,
            )

        if isinstance(exception, DuplicateColorNameInProductException):
            return ApiResponse(
                code=ApiCode.VARIANT_DUPLICATE_COLOR_NAME_IN_PRODUCT,
                message="A variant with this color name already exists for this product.",
                status=409,
            )

        if isinstance(exception, UnsupportedImageContentTypeException):
            return ApiResponse(
                code=ApiCode.UNSUPPORTED_IMAGE_CONTENT_TYPE,
                message=exception.message,
                status=400,
            )

        if isinstance(exception, ImagesSizeLimitExceededException):
            return ApiResponse(
                code=ApiCode.IMAGES_SIZE_LIMIT_EXCEEDED,
                message=exception.message,
                status=413,
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