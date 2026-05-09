from django.db import OperationalError, transaction

from classification_app.apis.filter.deactivate_filter.dtos import DeactivateFilterResponseDTO
from classification_app.apis.filter.deactivate_filter.exception import FilterAlreadyInactiveException
from classification_app.errors import FilterNotFoundException
from classification_app.models import Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class DeactivateFilterService:
    @transaction.atomic
    def execute(self, filter_id: int) -> DeactivateFilterResponseDTO:
        filter_obj = self._find_filter(filter_id)

        if not filter_obj.is_active:
            raise FilterAlreadyInactiveException()

        try:
            filter_obj.is_active = False
            filter_obj.save(update_fields=["is_active"])

            filter_values_deactivated = filter_obj.values.filter(is_active=True).update(is_active=False)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return DeactivateFilterResponseDTO(
            filter_id=filter_obj.id,
            is_active=filter_obj.is_active,
            filter_values_deactivated=filter_values_deactivated,
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