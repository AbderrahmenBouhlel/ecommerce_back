from datetime import datetime
from core.apiResponse.response import BaseDTO


class FilterValueItemDTO(BaseDTO):
    def __init__(self, id: int, value: str, slug: str, is_active: bool, created_at: datetime):
        self.id = id
        self.value = value
        self.slug = slug
        self.is_active = is_active
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "value": self.value,
            "slug": self.slug,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }


class FilterItemDTO(BaseDTO):
    def __init__(self, id: int, name: str, slug: str, description: str | None, is_active: bool, filter_values: list[FilterValueItemDTO]):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.filter_values = filter_values

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "is_active": self.is_active,
            "filter_values": [fv.to_dict() for fv in self.filter_values],
        }


class GetCategoryAllowedFiltersResponseDTO(BaseDTO):
    def __init__(self, filters: list[FilterItemDTO]):
        self.filters = filters

    def to_dict(self) -> list[dict]:
        return [f.to_dict() for f in self.filters]
