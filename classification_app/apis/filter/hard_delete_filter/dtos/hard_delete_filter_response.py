from core.apiResponse.response import BaseDTO


class HardDeleteFilterResponseDTO(BaseDTO):
    def __init__(
        self,
        filter_id: int,
        affected_products: int,
        affected_categories: int,
        affected_filter_values: int,
    ):
        self.filter_id = filter_id
        self.affected_products = affected_products
        self.affected_categories = affected_categories
        self.affected_filter_values = affected_filter_values

    def to_dict(self) -> dict:
        return {
            "filterId": self.filter_id,
            "affected": {
                "products": self.affected_products,
                "categories": self.affected_categories,
                "filterValues": self.affected_filter_values,
            },
        }
