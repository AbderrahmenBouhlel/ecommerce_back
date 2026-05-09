import re
from typing import List
from django.core.files.uploadedfile import UploadedFile

from core.exceptions.excecptions import RequestValidationException
from product_app.apis.create_product_variant.exception.exception import (
    ImagesSizeLimitExceededException,
    UnsupportedImageContentTypeException,
)


class CreateProductVariantRequestDTO:
    SUPPORTED_CONTENT_TYPES = ["image/jpeg", "image/png"]
    MAX_TOTAL_PAYLOAD_SIZE_MB = 10

    def __init__(self, data: dict, id: object):
        self.color_name = self._validate_color_name(data.get("color_name"))
        self.color_code = self._validate_color_code(data.get("color_code"))
        self.images: List[UploadedFile] = data.get("images", [])

        self.id = self._validate_id(id)

        self.__assert_empty_images()
        self.__assert_valid_images_content_type()
        self.__assert_total_payload_size_limit()

    @classmethod
    def from_request(cls, request, id: object) -> "CreateProductVariantRequestDTO":
        if not request.content_type or "multipart/form-data" not in request.content_type.lower():
            raise RequestValidationException(
                message="Content-Type must be multipart/form-data for file uploads.",
                cause=None,
            )

        uploaded_images: List[UploadedFile] = request.FILES.getlist("images") if "images" in request.FILES else []

        color_name = request.POST.get("color_name")
        color_code = request.POST.get("color_code")

        return cls(
            {
                "images": uploaded_images,
                "color_name": color_name,
                "color_code": color_code,
            },
            id,
        )

    # -------------------------
    # Validation helpers
    # -------------------------

    def __assert_empty_images(self):
        if not self.images:
            raise RequestValidationException(
                message="At least one image file must be uploaded.",
                cause=None,
            )

    def __assert_valid_images_content_type(self):
        for image in self.images:
            if image.content_type not in self.SUPPORTED_CONTENT_TYPES:
                raise UnsupportedImageContentTypeException(
                    message=(
                        f"Unsupported image content type: {image.content_type}. "
                        f"Supported types are: {', '.join(self.SUPPORTED_CONTENT_TYPES)}."
                    ),
                    cause=None,
                )

    def __assert_total_payload_size_limit(self):
        total_size = sum(image.size for image in self.images)
        max_size_bytes = self.MAX_TOTAL_PAYLOAD_SIZE_MB * 1024 * 1024

        if total_size > max_size_bytes:
            raise ImagesSizeLimitExceededException(
                message=f"Total payload size exceeds {self.MAX_TOTAL_PAYLOAD_SIZE_MB}MB limit.",
                cause=None,
            )

    # -------------------------
    # Field validation
    # -------------------------

    def _validate_color_name(self, value: object) -> str:
        if not value or not isinstance(value, str):
            self._invalid_request("Color name is required and must be a non-empty string.")

        normalized = value.strip()

        if len(normalized) < 1 or len(normalized) > 255:
            self._invalid_request("Color name must be between 1 and 255 characters.")

        return normalized

    def _validate_color_code(self, value: object) -> str:
        if not value or not isinstance(value, str):
            self._invalid_request("Color code is required and must be a string.")

        normalized = value.strip()

        if not re.match(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", normalized):
            self._invalid_request("Color code must be a valid hex code, e.g., '#ffffff'.")

        return normalized

    def _validate_id(self, value: object) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            self._invalid_request("Invalid product id.")

    def _invalid_request(self, message: str):
        raise RequestValidationException(
            message=message,
            cause=None,
        )
        if value is None:
            self._invalid_request("Product ID is required.")

        try:
            value_int = int(value)
            if value_int <= 0:
                self._invalid_request("Product ID must be a positive integer.")
                
            return value_int
        except (ValueError, TypeError):
            self._invalid_request("Product ID must be a valid integer.")