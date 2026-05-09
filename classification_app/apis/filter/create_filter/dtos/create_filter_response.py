from datetime import datetime

from core.apiResponse.response import BaseDTO


class CreateFilterResponseDTO(BaseDTO):
    def __init__(self, id: int, name: str, description: str, createdAt: datetime ,slug: str, isActive: bool):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = createdAt
        self.slug = slug
        self.is_active = isActive


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "createdAt": self.created_at.isoformat(),
            "slug": self.slug,
            "isActive": self.is_active
        }