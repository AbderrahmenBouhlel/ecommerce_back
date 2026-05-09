from core.apiResponse.response import BaseDTO


class CategorySelectItemDTO(BaseDTO):
    def __init__(self, id: int, name: str, gender: str, is_active: bool , slug: str):
        self.id = id
        self.name = name
        self.gender = gender
        self.is_active = is_active
        self.slug = slug

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "isActive": self.is_active,
            "slug": self.slug,
        }


class GetAllCategoriesSelectResponseDTO(BaseDTO):
    def __init__(self, categories: list[CategorySelectItemDTO]):
        self.categories = categories

    def to_dict(self) -> list[dict]:
        return [item.to_dict() for item in self.categories]
