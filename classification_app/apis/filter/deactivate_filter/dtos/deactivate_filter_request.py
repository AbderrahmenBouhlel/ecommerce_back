from core.exceptions.excecptions import RequestValidationException


class DeactivateFilterRequestDTO:
    def __init__(self, filter_id: int):
        if not isinstance(filter_id, int) or filter_id <= 0:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        self.filter_id = filter_id

    @classmethod
    def from_request(cls, filter_id: int) -> "DeactivateFilterRequestDTO":
        return cls(filter_id=filter_id)