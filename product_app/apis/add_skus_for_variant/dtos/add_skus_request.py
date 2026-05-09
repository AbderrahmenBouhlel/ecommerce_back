from typing import List
from core.exceptions.excecptions import RequestValidationException


class AddSkusForVariantRequestDTO:
    def __init__(self, data: dict, variant_id: object):
        self.skus = data.get("skus", [])
        self.variant_id = self._validate_id(variant_id)

        self.__assert_skus_present()
        self.__assert_skus_structure()
        self.__assert_no_duplicate_sizes()

    @classmethod
    def from_request(cls, request, variant_id: object):
        if not request.content_type or "application/json" not in request.content_type:
            raise RequestValidationException(message="Content-Type must be application/json.", cause=None)

        try:
            body = request.body.decode('utf-8') if hasattr(request.body, 'decode') else request.body
            import json
            parsed = json.loads(body) if body else {}
        except Exception as e:
            raise RequestValidationException(message="Invalid JSON body.", cause=e)

        return cls(parsed, variant_id)

    def __assert_skus_present(self):
        if not isinstance(self.skus, list) or not self.skus:
            raise RequestValidationException(message="'skus' must be a non-empty list.", cause=None)

    def __assert_skus_structure(self):
        for sku in self.skus:
            if not isinstance(sku, dict):
                raise RequestValidationException(message="Each SKU must be an object with 'size' and 'stock'.", cause=None)
            if 'size' not in sku or not sku['size'] or not isinstance(sku['size'], str):
                raise RequestValidationException(message="SKU 'size' is required and must be a string.", cause=None)
            if 'stock' not in sku:
                raise RequestValidationException(message="SKU 'stock' is required.", cause=None)
            try:
                sku['stock'] = int(sku['stock'])
            except Exception:
                raise RequestValidationException(message="SKU 'stock' must be an integer.", cause=None)
            if sku['stock'] < 0:
                raise RequestValidationException(message="Stock cannot be negative.", cause=None)


    def __assert_no_duplicate_sizes(self):
        seen_sizes = set()
        for sku in self.skus:
            size = sku['size']
            if size in seen_sizes:
                raise RequestValidationException(message=f"Duplicate size '{size}' found in request.", cause=None)
            seen_sizes.add(size)
    def _validate_id(self, value: object) -> int:
        if value is None or isinstance(value, bool):
            raise RequestValidationException(
                message="Variant ID is required and must be a valid integer.",
                cause=None,
            )

        if isinstance(value, float):
            raise RequestValidationException(
                message="Variant ID must be a valid integer.",
                cause=None,
            )

        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise RequestValidationException(
                message="Variant ID must be a valid integer.",
                cause=None,
            )

        if parsed <= 0:
            raise RequestValidationException(
                message="Variant ID must be a positive integer.",
                cause=None,
            )

        return parsed

