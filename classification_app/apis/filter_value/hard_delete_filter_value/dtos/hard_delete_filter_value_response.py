from core.apiResponse.response import BaseDTO


class HardDeleteFilterValueResponseDTO(BaseDTO):
    def __init__(
        self,
        filter_value_id: int,
        affected_products: int,
    ):
        self.filter_value_id = filter_value_id
        self.affected_products = affected_products

    def to_dict(self) -> dict:
        return {
            "filterValueId": self.filter_value_id,
            "affected": {
                "affectedProducts": self.affected_products,
            },
        }
