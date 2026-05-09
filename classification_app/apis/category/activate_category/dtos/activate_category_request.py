from core.exceptions.excecptions import RequestValidationException


class ActivateCategoryRequestDTO:
    def __init__(self, category_id: int):
        if not isinstance(category_id, int) or category_id <= 0:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        self.category_id = category_id

    @classmethod
    def from_request(cls, category_id: int) -> "ActivateCategoryRequestDTO":
        return cls(category_id=category_id)