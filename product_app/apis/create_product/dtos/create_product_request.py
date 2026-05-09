import json
from decimal import Decimal, InvalidOperation

from core.exceptions.excecptions import RequestValidationException


class CreateProductRequestDTO:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.description = data.get("description")
        self.price = data.get("price")
        self.category_id = data.get("categoryId")

        self.name = self._validate_name(self.name)
        self.description = self._validate_description(self.description)
        self.price = self._validate_price(self.price)
        self.category_id = self._validate_category_id(self.category_id)

    @classmethod
    def from_request(cls, request) -> "CreateProductRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(data)

    def _invalid_request(self , message: str) -> None:
        raise RequestValidationException(
            message=message,
            cause=None,
        )

    def _validate_name(self, value: object) -> str:
        if value is None or not isinstance(value, str):
            self._invalid_request("Product name is required and must be a string.")

        normalized = value.strip()
        if len(normalized) < 3 or len(normalized) > 255:
            self._invalid_request("Product name must be between 3 and 255 characters.")

        return normalized

    def _validate_description(self, value: object) -> str:
        if value is None:
            return ""

        if not isinstance(value, str):
            self._invalid_request("Product description must be a string.")

        normalized = value.strip()
        if len(normalized) > 2000:
            self._invalid_request("Product description must be less than 2000 characters.")

        return normalized

    def _validate_price(self, value: object) -> Decimal:
        if value is None or isinstance(value, bool):
            self._invalid_request("Product price is required and must be a valid decimal number.")

        try:
            parsed = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            self._invalid_request("Product price must be a valid decimal number.")

        if parsed < 0:
            self._invalid_request("Product price must be a positive decimal number.")

        if parsed.as_tuple().exponent < -2:
            self._invalid_request("Product price must have at most two decimal places.")

        return parsed

    def _validate_category_id(self, value: object) -> int:
        if value is None or isinstance(value, bool):
            self._invalid_request("Product category ID is required and must be a valid integer.")

        if isinstance(value, float):
            self._invalid_request("Product category ID must be a valid integer.")

        try:
            parsed = int(value)
        except (ValueError, TypeError):
            self._invalid_request("Product category ID must be a valid integer.")

        if parsed <= 0:
            self._invalid_request("Product category ID must be a positive integer.")

        return parsed