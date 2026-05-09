from core.exceptions.excecptions import RequestValidationException

from classification_app.errors import ConfirmationRequiredException


class HardDeleteFilterRequestDTO:
    def __init__(self, filter_id: int, confirm_raw: str | None):
        if not isinstance(filter_id, int) or filter_id <= 0:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        if confirm_raw is None :
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        normalized = str(confirm_raw).strip().lower()

        if normalized in {"true", "1", "yes"}:
            self.confirm = True
        elif normalized in {"false", "0", "no"}:
            self.confirm = False
        else:
            raise RequestValidationException(
                message="Invalid request. dues to missing or invalid parameters.",
                cause=None,
            )

        if not self.confirm:
            raise ConfirmationRequiredException()

        self.filter_id = filter_id

    @classmethod
    def from_request(cls, request, filter_id: int) -> "HardDeleteFilterRequestDTO":
        confirm_raw = request.GET.get("confirm")
        return cls(filter_id=filter_id, confirm_raw=confirm_raw)
