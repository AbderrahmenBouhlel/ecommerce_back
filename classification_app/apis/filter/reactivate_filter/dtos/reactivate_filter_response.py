from core.apiResponse.response import BaseDTO


class ReactivateFilterResponseDTO(BaseDTO):
    def __init__(self, filter_id: int, is_active: bool):
        self.filter_id = filter_id
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "filterId": self.filter_id,
            "isActive": self.is_active,
            "note": "Filter values remain inactive until explicitly reactivated.",
        }