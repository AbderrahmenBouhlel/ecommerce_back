from datetime import datetime

from core.apiResponse.response import BaseDTO


class CategoryAllowedFilterDTO(BaseDTO):
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


class CategoryItemDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        name: str,
        gender: str,
        slug: str,
        description: str,
        is_active: bool,
        created_at: datetime,
        allowed_filters: list[CategoryAllowedFilterDTO],
    ):
        self.id = id
        self.name = name
        self.gender = gender
        self.slug = slug
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.allowed_filters = allowed_filters

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "slug": self.slug,
            "description": self.description,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
            "allowedFilters": [filter_item.to_dict() for filter_item in self.allowed_filters],
        }


class GetAllCategoriesResponseDTO(BaseDTO):
    def __init__(self, categories: list[CategoryItemDTO]):
        self.categories = categories

    def to_dict(self) -> list[dict]:
        return [item.to_dict() for item in self.categories]