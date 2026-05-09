from core.apiResponse.response import BaseDTO


class DisableCategoryFilterResponseDTO(BaseDTO):
    def __init__(self, category_id: int, filter_id: int, affected_products_count: int):
        self.category_id = category_id
        self.filter_id = filter_id
        self.affected_products_count = affected_products_count

    def to_dict(self) -> dict:
        return {
            "categoryId": self.category_id,
            "filterId": self.filter_id,
            "affectedProductsCount": self.affected_products_count,
        }