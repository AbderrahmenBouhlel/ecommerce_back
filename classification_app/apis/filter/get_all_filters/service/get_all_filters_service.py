from django.db import OperationalError
from django.db.models import Prefetch

from classification_app.apis.filter.get_all_filters.dtos import (
    GetAllFiltersResponseDTO,
    FilterItemDTO,
    FilterValueItemDTO,
)
from classification_app.models import Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class GetAllFiltersService:
    def execute(self) -> GetAllFiltersResponseDTO:
        filters = self._find_all_filters_with_values()

        filter_items: list[FilterItemDTO] = []

        for filter_obj in filters:
            values = [
                FilterValueItemDTO(
                    id=value.id,
                    name=value.name,
                    slug=value.slug,
                    description=value.description,
                    is_active=value.is_active,
                    created_at=value.created_at,
                )
                for value in filter_obj.values.all()
            ]

            filter_items.append(
                FilterItemDTO(
                    id=filter_obj.id,
                    name=filter_obj.name,
                    slug=filter_obj.slug,
                    description=filter_obj.description,
                    is_active=filter_obj.is_active,
                    created_at=filter_obj.created_at,
                    values=values,
                )
            )

        return GetAllFiltersResponseDTO(filters=filter_items)

    def _find_all_filters_with_values(self):
        try:
            return Filter.objects.prefetch_related("values")
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
