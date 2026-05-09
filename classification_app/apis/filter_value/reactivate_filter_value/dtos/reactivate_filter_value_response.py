from core.apiResponse.response import BaseDTO


class ReactivateFilterValueResponseDTO(BaseDTO):
    def __init__(self, filter_value_id: int, is_active: bool):
        self.filter_value_id = filter_value_id
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "filterValueId": self.filter_value_id,
            "isActive": self.is_active,
        }