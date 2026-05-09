from core.apiResponse.response import BaseDTO


class EnableCategoryFilterResponseDTO(BaseDTO):
    def __init__(self, category_id: int, filter_id: int):
        self.category_id = category_id
        self.filter_id = filter_id

    def to_dict(self) -> dict:
        return {
            "categoryId": self.category_id,
            "filterId": self.filter_id,
        }