from core.exceptions.excecptions import RequestValidationException


class DisableCategoryFilterRequestDTO:
    def __init__(self, category_id: int, filter_id: int):
        if not isinstance(category_id, int) or category_id <= 0:
            raise RequestValidationException(
                message="Invalid request parameters.",
                cause=None,
            )

        if not isinstance(filter_id, int) or filter_id <= 0:
            raise RequestValidationException(
                message="Invalid request parameters.",
                cause=None,
            )

        self.category_id = category_id
        self.filter_id = filter_id

    @classmethod
    def from_request(cls, category_id: int, filter_id: int) -> "DisableCategoryFilterRequestDTO":
        return cls(category_id=category_id, filter_id=filter_id)