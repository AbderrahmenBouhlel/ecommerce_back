from django.db import OperationalError
from django.db.models import Prefetch

from classification_app.apis.category.get_all_categories.dtos import (
    CategoryAllowedFilterDTO,
    CategoryItemDTO,
    GetAllCategoriesResponseDTO,
)
from classification_app.models import Category, CategoryFilter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class GetAllCategoriesService:
    def execute(self) -> GetAllCategoriesResponseDTO:
        categories = self._find_all_categories_with_filters()

        category_items: list[CategoryItemDTO] = []

        for category_obj in categories:
            allowed_filters = [
                CategoryAllowedFilterDTO(
                    id=category_filter.filter.id,
                    name=category_filter.filter.name,
                    slug=category_filter.filter.slug,
                    description=category_filter.filter.description,
                    is_active=category_filter.filter.is_active,
                    created_at=category_filter.filter.created_at,
                )
                for category_filter in category_obj.category_filters.all()
            ]

            category_items.append(
                CategoryItemDTO(
                    id=category_obj.id,
                    name=category_obj.name,
                    gender=category_obj.gender,
                    slug=category_obj.slug,
                    description=category_obj.description,
                    is_active=category_obj.is_active,
                    created_at=category_obj.created_at,
                    allowed_filters=allowed_filters,
                )
            )

        return GetAllCategoriesResponseDTO(categories=category_items)

    def _find_all_categories_with_filters(self):
        try:
            return Category.objects.prefetch_related(
                Prefetch(
                    "category_filters",
                    queryset=CategoryFilter.objects.select_related("filter"),
                )
            )
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)