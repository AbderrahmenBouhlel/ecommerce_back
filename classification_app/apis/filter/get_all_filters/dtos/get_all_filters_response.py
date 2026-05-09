from datetime import datetime

from core.apiResponse.response import BaseDTO


class FilterValueItemDTO(BaseDTO):
    def __init__(self, id: int, name: str, slug: str, description: str, is_active: bool, created_at: datetime):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
        }


class FilterItemDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        description: str,
        is_active: bool,
        created_at: datetime,
        values: list[FilterValueItemDTO],
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.values = values

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
            "values": [value.to_dict() for value in self.values],
        }


class GetAllFiltersResponseDTO(BaseDTO):
    def __init__(self, filters: list[FilterItemDTO]):
        self.filters = filters

    def to_dict(self) -> list[dict]:
        return [item.to_dict() for item in self.filters]
