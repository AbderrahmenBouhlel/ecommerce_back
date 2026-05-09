from django.db import OperationalError

from classification_app.apis.filter_value.reactivate_filter_value.dtos import ReactivateFilterValueResponseDTO
from classification_app.apis.filter_value.reactivate_filter_value.exception import (
    FilterValueAlreadyActiveException
)
from classification_app.errors import FilterValueNotFoundException 
from classification_app.models import FilterValue
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class ReactivateFilterValueService:
    def execute(self, filter_value_id: int) -> ReactivateFilterValueResponseDTO:
        filter_value = self._find_filter_value(filter_value_id)

        if filter_value.is_active:
            raise FilterValueAlreadyActiveException()

        try:
            filter_value.is_active = True
            filter_value.save(update_fields=["is_active"])
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ReactivateFilterValueResponseDTO(
            filter_value_id=filter_value.id,
            is_active=filter_value.is_active,
        )

    def _find_filter_value(self, filter_value_id: int) -> FilterValue:
        try:
            return FilterValue.objects.get(id=filter_value_id)
        except FilterValue.DoesNotExist as e:
            raise FilterValueNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)