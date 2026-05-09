from core.apiResponse.response import BaseDTO
from auth_app.dtos import UserProfileDTO
    
    

        
class SignupResponseDTO(BaseDTO):
    def __init__(self, token: str, id: str, email: str, name: str, role: str):
        self.token = token
        self.user_profile = UserProfileDTO(id=id, email=email, name=name, role=role)
    

    def to_dict(self):
        return {
            "token": self.token,
            "userProfile": self.user_profile.to_dict(),
        }