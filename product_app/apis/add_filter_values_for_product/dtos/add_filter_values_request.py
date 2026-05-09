from core.exceptions.excecptions import RequestValidationException


class AddFilterValuesForProductRequestDTO:
    def __init__(self, data: dict, product_id: object):
        self.filter_values = data.get("filter_values", [])
        self.product_id = self._validate_id(product_id)

        self.__assert_filter_values_present()
        self.__assert_filter_values_structure()

    @classmethod
    def from_request(cls, request, product_id: object):
        if not request.content_type or "application/json" not in request.content_type:
            raise RequestValidationException(message="Content-Type must be application/json.", cause=None)

        try:
            body = request.body.decode('utf-8') if hasattr(request.body, 'decode') else request.body
            import json
            parsed = json.loads(body) if body else {}
        except Exception as e:
            raise RequestValidationException(message="Invalid JSON body.", cause=e)

        return cls(parsed, product_id)

    def __assert_filter_values_present(self):
        if not isinstance(self.filter_values, list) or not self.filter_values:
            raise RequestValidationException(message="'filter_values' must be a non-empty list.", cause=None)

    def __assert_filter_values_structure(self):
        for item in self.filter_values:
            if not isinstance(item, dict):
                raise RequestValidationException(message="Each item in 'filter_values' must be an object with 'filter_value_id'.", cause=None)
            if 'filter_value_id' not in item:
                raise RequestValidationException(message="Each filter value must include 'filter_value_id'.", cause=None)
            try:
                item['filter_value_id'] = int(item['filter_value_id'])
            except Exception:
                raise RequestValidationException(message="'filter_value_id' must be an integer.", cause=None)

    def _validate_id(self, value: object) -> int:
        if value is None or isinstance(value, bool):
            raise RequestValidationException(
                message="Product ID is required and must be a valid integer.",
                cause=None,
            )

        if isinstance(value, float):
            raise RequestValidationException(
                message="Product ID must be a valid integer.",
                cause=None,
            )

        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise RequestValidationException(
                message="Product ID must be a valid integer.",
                cause=None,
            )

        if parsed <= 0:
            raise RequestValidationException(
                message="Product ID must be a positive integer.",
                cause=None,
            )

        return parsed
