import json

from django.utils.text import slugify

from core.exceptions.excecptions import RequestValidationException


class CreateFilterValueRequestDTO:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.description = data.get("description")

        if self.name is None or not isinstance(self.name, str) or not self.name.strip():
            raise RequestValidationException(
                message="Invalid filter value request.",
                cause=None,
            )
        if self.description is None or not isinstance(self.description, str):
            raise RequestValidationException(
                message="Invalid filter value request.",
                cause=None,
            )

        self.name = self.name.strip()
        self.description = self.description.strip()


    @classmethod
    def from_request(cls, request) -> "CreateFilterValueRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(data)
