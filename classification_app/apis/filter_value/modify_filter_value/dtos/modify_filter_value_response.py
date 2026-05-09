from datetime import datetime

from core.apiResponse.response import BaseDTO


class ModifyFilterValueResponseDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        filter_id: int,
        name: str,
        slug: str,
        description: str,
        is_active: bool,
        updated_at: datetime,
    ):
        self.id = id
        self.filter_id = filter_id
        self.name = name
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filterId": self.filter_id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "isActive": self.is_active,
            "updatedAt": self.updated_at.isoformat()
        }