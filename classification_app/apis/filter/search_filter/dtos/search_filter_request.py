import json

from core.exceptions.excecptions import RequestValidationException


class SearchFilterRequestDTO:
    def __init__(self, data: dict):
        print(data)
        
        q = data.get("q")
        if q is None or not isinstance(q, str):
            raise RequestValidationException(
                message="Invalid search filter request.",
                cause=None,
            )
        self.q = q.strip()
        
        excluded_ids = data.get("excludedIds", [])
        if not isinstance(excluded_ids, list) or not all(isinstance(id, int) and id > 0 for id in excluded_ids):
            raise RequestValidationException(
                message="Invalid search filter request.",
                cause=None,
            )
            
        self.excluded_ids = excluded_ids

    @classmethod
    def from_request(cls, request) -> "SearchFilterRequestDTO":
        if request.content_type and request.content_type.startswith("application/json"):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        else:
            data = request.POST.dict()

        return cls(data=data)
       