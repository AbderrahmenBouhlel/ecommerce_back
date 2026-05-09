import json

from core.exceptions.excecptions import RequestValidationException


class ModifyFilterValueRequestDTO:
    def __init__(self, filter_value_id: int, data: dict):
        self.filter_value_id = filter_value_id
        self.name = data.get("name")
        self.description = data.get("description")

        if not isinstance(filter_value_id, int) or filter_value_id <= 0:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        has_name = "name" in data
        has_description = "description" in data

        if not has_name and not has_description:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        if has_name:
            if self.name is None or not isinstance(self.name, str) or not self.name.strip():
                raise RequestValidationException(
                    message="Invalid request. dues to missing or invalid parameters.",
                    cause=None,
                )
            self.name = self.name.strip()

        if has_description:
            if self.description is None or not isinstance(self.description, str) or not self.description.strip():
                raise RequestValidationException(
                    message="Invalid request. dues to missing or invalid parameters.",
                    cause=None,
                )
            self.description = self.description.strip()

    @classmethod
    def from_request(cls, request, filter_value_id: int) -> "ModifyFilterValueRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(filter_value_id=filter_value_id, data=data)