from core.exceptions.excecptions import RequestValidationException
import json


import json
from core.exceptions.excecptions import RequestValidationException


class SignupRequestDTO:
    def __init__(self, data: dict):
        self.email = data.get("email")
        self.password = data.get("password")
        self.name = data.get("name")

        # Shape / type validation only
        if self.email is None or not isinstance(self.email, str):
            raise RequestValidationException(message="Field 'email' is required and must be a string.", cause=None)

        if self.password is None or not isinstance(self.password, str):
            raise RequestValidationException(message="Field 'password' is required and must be a string.", cause=None)

        if self.name is None or not isinstance(self.name, str):
            raise RequestValidationException(message="Field 'name' is required and must be a string.", cause=None)

    @classmethod
    def from_request(cls, request) -> "SignupRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                raw = request.body.decode("utf-8")
                data = json.loads(raw) if raw else {}
            except (UnicodeDecodeError, json.JSONDecodeError):
                data = {}
        else:
            data = request.POST.dict()

        return cls(data)