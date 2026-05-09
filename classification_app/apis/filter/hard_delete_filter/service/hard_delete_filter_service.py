from django.db import OperationalError, transaction

from classification_app.errors import FilterNotFoundException
from classification_app.apis.filter.hard_delete_filter.dtos import HardDeleteFilterResponseDTO

from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from classification_app.models import Filter , FilterValue, CategoryFilter
from product_app.models import ProductFilterValue

class HardDeleteFilterService:
    @transaction.atomic
    def execute(self, filter_id: int) -> HardDeleteFilterResponseDTO:
        filter = self._find_filter(filter_id)


        try:
            filter_values_ids = list(
                FilterValue.objects
                .filter(filter=filter)
                .values_list('id', flat=True)
            )

            affected_filter_values = len(filter_values_ids)

            if filter_values_ids:
                affected_categories = CategoryFilter.objects.filter(
                    filter_id=filter.id
                ).values("category_id").distinct().count()

                affected_products = ProductFilterValue.objects.filter(
                    filter_value_id__in=filter_values_ids
                ).values("product_id").distinct().count()
            else:
                affected_categories = 0
                affected_products = 0

            filter.delete()
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return HardDeleteFilterResponseDTO(
            filter_id=filter.id,
            affected_products=affected_products,
            affected_categories=affected_categories,
            affected_filter_values=affected_filter_values,  # Assuming no filter values are deleted
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
