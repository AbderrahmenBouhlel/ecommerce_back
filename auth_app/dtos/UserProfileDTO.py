from core.apiResponse.response import BaseDTO



class UserProfileDTO(BaseDTO):
    def __init__(self, id: int, email: str, name: str, role: str):
        self.id = id
        self.email = email
        self.name = name
        self.role = role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role
        }
        
        
    @staticmethod
    def from_entity(user) -> 'UserProfileDTO':
        return UserProfileDTO(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role
        )