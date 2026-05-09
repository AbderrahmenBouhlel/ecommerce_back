from core.exceptions.excecptions import RequestValidationException
import json


class LoginRequestDTO:
    def __init__(self, data: dict):
        self.email = data.get("email")
        self.password = data.get("password")
        
        # STRICT VALIDATION: Check if keys exist and are not empty
        if not self.email or not isinstance(self.email, str):
            raise RequestValidationException("Field 'email' is required and must be a string.", "BAD_REQUEST")
            
        if not self.password or not isinstance(self.password, str):
            raise RequestValidationException("Field 'password' is required and must be a string.", "BAD_REQUEST")
 
    @classmethod
    def from_request(cls, request) -> 'LoginRequestDTO':
        # Check if the client sent JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            # Fallback to standard Form data
            data = request.POST.dict()
        
        return cls(data)