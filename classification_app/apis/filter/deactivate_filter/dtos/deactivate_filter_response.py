from core.apiResponse.response import BaseDTO


class DeactivateFilterResponseDTO(BaseDTO):
    def __init__(self, filter_id: int, is_active: bool, filter_values_deactivated: int):
        self.filter_id = filter_id
        self.is_active = is_active
        self.filter_values_deactivated = filter_values_deactivated

    def to_dict(self) -> dict:
        return {
            "filterId": self.filter_id,
            "isActive": self.is_active,
            "affected": {
                "filterValuesDeactivated": self.filter_values_deactivated,
            },
        }