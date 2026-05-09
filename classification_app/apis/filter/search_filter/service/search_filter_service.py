from django.db import OperationalError

from classification_app.apis.filter.search_filter.dtos import SearchFilterItemDTO, SearchFiltersResponseDTO
from classification_app.models import Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class SearchFilterService:
    def execute(self, q: str, excluded_ids: list[int]) -> SearchFiltersResponseDTO:
        print(f"Executing SearchFilterService with q='{q}' and excluded_ids={excluded_ids}")
        filters = self._find_filters(search_term=q, exclude_ids=excluded_ids)

        filter_items = [
            SearchFilterItemDTO(
                id=filter_obj.id,
                name=filter_obj.name,
                slug=filter_obj.slug,
                description=filter_obj.description,
                created_at=filter_obj.created_at,
            )
            for filter_obj in filters
        ]

        return SearchFiltersResponseDTO(filters=filter_items)



    def _find_filters(self, search_term: str, exclude_ids: list[int]):
        try:
            queryset = Filter.objects.filter(is_active=True)
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)

            if exclude_ids:
                queryset = queryset.exclude(id__in=exclude_ids)
                print(queryset)

            return queryset.order_by("name")
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)