from typing import List
from core.apiResponse.response import BaseDTO


class ProductFilterValueDTO(BaseDTO):
    def __init__(self, id: int, product_id: int, filter_value_id: int, filter_value_name: str):
        self.id = id
        self.product_id = product_id
        self.filter_value_id = filter_value_id
        self.filter_value_name = filter_value_name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "filter_value_id": self.filter_value_id,
            "filter_value_name": self.filter_value_name,
        }


class AddFilterValuesForProductResponseDTO(BaseDTO):
    def __init__(self, assignments: List[ProductFilterValueDTO]):
        self.assignments = assignments

    def to_dict(self) -> list[dict]:
        return [a.to_dict() for a in self.assignments]
