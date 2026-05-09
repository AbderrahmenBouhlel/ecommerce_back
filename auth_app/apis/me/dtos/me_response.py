from core.apiResponse.response import BaseDTO
from auth_app.dtos import UserProfileDTO
    
    
class MeResponseDTO(BaseDTO):
    def __init__(self, id: int, email: str, name: str , role: str):
        self.user_profile = UserProfileDTO(id=id, email=email, name=name, role=role)

    def to_dict(self) -> dict:
        return {
            "user_profile": self.user_profile.to_dict()
        }