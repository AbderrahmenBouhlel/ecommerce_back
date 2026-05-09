from core.exceptions.excecptions import RequestValidationException


class ReactivateFilterValueRequestDTO:
    def __init__(self, filter_value_id: int):
        if not isinstance(filter_value_id, int) or filter_value_id <= 0:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        self.filter_value_id = filter_value_id

    @classmethod
    def from_request(cls, filter_value_id: int) -> "ReactivateFilterValueRequestDTO":
        return cls(filter_value_id=filter_value_id)