import json

from core.exceptions.excecptions import RequestValidationException


class CreateCategoryRequestDTO:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.gender = data.get("gender")
        self.description = data.get("description")

        if self.name is None or not isinstance(self.name, str) or not self.name.strip():
            raise RequestValidationException(
                message="Invalid category creation request.",
                cause=None,
            )

        if self.gender is None or not isinstance(self.gender, str):
            raise RequestValidationException(
                message="Invalid category creation request.",
                cause=None,
            )

        if self.description is None or not isinstance(self.description, str):
            raise RequestValidationException(
                message="Invalid category creation request.",
                cause=None,
            )

        self.name = self.name.strip()
        self.gender = self.gender.strip().upper()
        self.description = self.description.strip()

        if self.gender not in {"MALE", "FEMALE"}:
            raise RequestValidationException(
                message="Invalid category creation request.",
                cause=None,
            )

    @classmethod
    def from_request(cls, request) -> "CreateCategoryRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(data)