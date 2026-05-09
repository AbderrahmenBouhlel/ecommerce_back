from datetime import datetime
from core.apiResponse.response import BaseDTO


class SearchFilterItemDTO(BaseDTO):
    def __init__(self, id: int, name: str, slug: str, description: str, created_at: datetime):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
        }


class SearchFiltersResponseDTO(BaseDTO):
    def __init__(self, filters: list[SearchFilterItemDTO]):
        self.filters = filters

    def to_dict(self) -> list[dict]:
        return [item.to_dict() for item in self.filters]