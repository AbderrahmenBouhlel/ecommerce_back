from core.apiResponse.response import BaseDTO
from auth_app.dtos import UserProfileDTO
    
    
class LoginResponseDTO(BaseDTO):
    def __init__(self, token: str, id: int, email: str, name: str , role: str):
        self.token = token
        self.user_profile = UserProfileDTO(id=id, email=email, name=name, role=role)

    def to_dict(self) -> dict:
        return {
            "token": self.token,
            "user_profile": self.user_profile.to_dict()
        }