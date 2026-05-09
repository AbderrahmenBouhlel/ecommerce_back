from django.db import OperationalError

from classification_app.apis.filter_value.deactivate_filter_value.dtos import DeactivateFilterValueResponseDTO
from classification_app.apis.filter_value.deactivate_filter_value.exception import (
    FilterValueAlreadyInactiveException,
)
from classification_app.errors import FilterValueNotFoundException 
from classification_app.models import FilterValue
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class DeactivateFilterValueService:
    def execute(self, filter_value_id: int) -> DeactivateFilterValueResponseDTO:
        filter_value = self._find_filter_value(filter_value_id)

        if not filter_value.is_active:
            raise FilterValueAlreadyInactiveException()

        try:
            filter_value.is_active = False
            filter_value.save(update_fields=["is_active"])
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return DeactivateFilterValueResponseDTO(
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