from core.apiResponse.response import BaseDTO


class DeactivateCategoryResponseDTO(BaseDTO):
    def __init__(self, category_id: int, is_active: bool):
        self.category_id = category_id
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "categoryId": self.category_id,
            "isActive": self.is_active,
        }