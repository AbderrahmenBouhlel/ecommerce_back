from django.db import OperationalError, transaction

from classification_app.apis.filter_value.hard_delete_filter_value.dtos import HardDeleteFilterValueResponseDTO
from classification_app.apis.filter_value.hard_delete_filter_value.exception import FilterValueNotFoundException
from classification_app.models import FilterValue
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class HardDeleteFilterValueService:
    @transaction.atomic
    def execute(self, filter_value_id: int) -> HardDeleteFilterValueResponseDTO:
        filter_value = self._find_filter_value(filter_value_id)

        affected_products = filter_value.products.count()

        try:
            filter_value.delete()
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return HardDeleteFilterValueResponseDTO(
            filter_value_id=filter_value_id,
            affected_products=affected_products,
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
