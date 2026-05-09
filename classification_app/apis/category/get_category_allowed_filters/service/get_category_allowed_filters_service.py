from django.db import OperationalError
from django.db.models import Prefetch

from classification_app.models import Category, CategoryFilter, FilterValue
from classification_app.apis.category.get_category_allowed_filters.dtos import (
    GetCategoryAllowedFiltersResponseDTO,
    FilterItemDTO,
    FilterValueItemDTO,
)
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from classification_app.errors import CategoryNotFoundException


class GetCategoryAllowedFiltersService:
    def execute(self, category_id: int) -> GetCategoryAllowedFiltersResponseDTO:
        category = self._find_category_with_filters(category_id)

        filters_list = []

        for category_filter in category.category_filters.all():
            filter = category_filter.filter

            # get filter values for this filter and category
            filter_values = FilterValue.objects.filter(filter_id=filter.id, is_active=True)

            fv_items = [
                FilterValueItemDTO(
                    id=fv.id,
                    value=fv.name,
                    slug=fv.slug,
                    is_active=fv.is_active,
                    created_at=fv.created_at,
                )
                for fv in filter_values
            ]

            filters_list.append(
                FilterItemDTO(
                    id=filter.id,
                    name=filter.name,
                    slug=filter.slug,
                    description=filter.description,
                    is_active=filter.is_active,
                    filter_values=fv_items,
                )
            )

        return GetCategoryAllowedFiltersResponseDTO(filters=filters_list)

    def _find_category_with_filters(self, category_id: int) -> Category:
        try:
            return Category.objects.prefetch_related(
                Prefetch(
                    "category_filters",
                    queryset=CategoryFilter.objects.select_related("filter"),
                )
            ).get(id=category_id)
        except Category.DoesNotExist as e:
            raise CategoryNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
