from datetime import datetime

from core.apiResponse.response import BaseDTO


class CreateFilterValueResponseDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        filter_id: int,
        name: str,
        description: str,
        slug: str,
        is_active: bool,
        created_at: datetime,
    ):
        self.id = id
        self.filter_id = filter_id
        self.name = name
        self.slug = slug
        self.is_active = is_active
        self.created_at = created_at
        self.description = description

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filterId": self.filter_id,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
        }
