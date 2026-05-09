from core.exceptions.excecptions import RequestValidationException

from classification_app.errors import ConfirmationRequiredException


class HardDeleteFilterValueRequestDTO:
    def __init__(self, filter_value_id: int, confirm_raw: str | None):
        if not isinstance(filter_value_id, int) or filter_value_id <= 0:
            raise RequestValidationException(
                message="Invalid filter value request. dues to missing or invalid parameters.",
                cause=None,
            )

        if confirm_raw is None :
            raise RequestValidationException(
                message="Invalid filter value request. dues to missing or invalid parameters.",
                cause=None,
            )

        normalized = str(confirm_raw).strip().lower()

        if normalized in {"true", "1", "yes"}:
            self.confirm = True
        elif normalized in {"false", "0", "no"}:
            self.confirm = False
        else:
            raise RequestValidationException(
                message="Invalid filter value request. dues to missing or invalid parameters.",
                cause=None,
            )

        if not self.confirm:
            raise ConfirmationRequiredException()

        self.filter_value_id = filter_value_id

    @classmethod
    def from_request(cls, request, filter_value_id: int) -> "HardDeleteFilterValueRequestDTO":
        confirm_raw = request.GET.get("confirm")
        return cls(filter_value_id=filter_value_id, confirm_raw=confirm_raw)
