from django.db import OperationalError

from classification_app.apis.filter.reactivate_filter.dtos import ReactivateFilterResponseDTO
from classification_app.apis.filter.reactivate_filter.exception import FilterAlreadyActiveException
from classification_app.errors import FilterNotFoundException
from classification_app.models import Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class ReactivateFilterService:
    def execute(self, filter_id: int) -> ReactivateFilterResponseDTO:
        filter_obj = self._find_filter(filter_id)

        if filter_obj.is_active:
            raise FilterAlreadyActiveException()

        try:
            filter_obj.is_active = True
            filter_obj.save(update_fields=["is_active"])
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ReactivateFilterResponseDTO(
            filter_id=filter_obj.id,
            is_active=filter_obj.is_active,
        )

    def _find_filter(self, filter_id: int) -> Filter:
        try:
            return Filter.objects.get(id=filter_id)
        except Filter.DoesNotExist as e:
            raise FilterNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)