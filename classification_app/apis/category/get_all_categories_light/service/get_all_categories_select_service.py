from django.db import OperationalError

from classification_app.apis.category.get_all_categories_light.dtos import (
    CategorySelectItemDTO,
    GetAllCategoriesSelectResponseDTO,
)
from classification_app.models import Category
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class GetAllCategoriesSelectService:
    def execute(self) -> GetAllCategoriesSelectResponseDTO:
        categories = self._find_all_categories()

        category_items: list[CategorySelectItemDTO] = []

        for category_obj in categories:
            category_items.append(
                CategorySelectItemDTO(
                    id=category_obj.id,
                    name=category_obj.name,
                    gender=category_obj.gender,
                    is_active=category_obj.is_active,
                    slug=category_obj.slug,
                )
            )

        return GetAllCategoriesSelectResponseDTO(categories=category_items)

    def _find_all_categories(self):
        try:
            return Category.objects.all()
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
