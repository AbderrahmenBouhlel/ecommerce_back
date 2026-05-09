from datetime import datetime

from core.apiResponse.response import BaseDTO


class CreateCategoryResponseDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        name: str,
        gender: str,
        slug: str,
        description: str,
        is_active: bool,
        created_at: datetime,
    ):
        self.id = id
        self.name = name
        self.gender = gender
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "slug": self.slug,
            "description": self.description,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
        }