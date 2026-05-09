import json

from core.exceptions.excecptions import RequestValidationException


class ModifyFilterRequestDTO:
    def __init__(self, filter_id: int, data: dict):
        self.filter_id = filter_id
        self.name = data.get("name")
        self.description = data.get("description")

        if not isinstance(filter_id, int) or filter_id <= 0:
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
            if self.description is None or not isinstance(self.description, str):
                raise RequestValidationException(
                    message="Invalid request. dues to missing or invalid parameters.",
                    cause=None,
                )
            self.description = self.description.strip()

    @classmethod
    def from_request(cls, request, filter_id: int) -> "ModifyFilterRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(filter_id=filter_id, data=data)