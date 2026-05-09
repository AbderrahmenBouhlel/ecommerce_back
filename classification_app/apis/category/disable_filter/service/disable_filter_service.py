from django.db import OperationalError, transaction

from classification_app.apis.category.disable_filter.dtos import DisableCategoryFilterResponseDTO
from classification_app.apis.category.disable_filter.exception import CategoryFilterNotAssociatedException
from classification_app.errors import CategoryNotFoundException, FilterNotFoundException
from classification_app.models import Category, CategoryFilter, Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from product_app.models import Product, ProductFilterValue


class DisableCategoryFilterService:
    @transaction.atomic
    def execute(self, category_id: int, filter_id: int) -> DisableCategoryFilterResponseDTO:
        category_obj = self._find_category(category_id)
        filter_obj = self._find_filter(filter_id)
        category_filter = self._find_category_filter(category_obj.id, filter_obj.id)

        try:
            affected_product_ids = list(
                Product.objects.filter(
                    category_id=category_obj.id,
                    filter_values__filter_value__filter_id=filter_obj.id,
                )
                .distinct()
                .values_list("id", flat=True)
            )

            ProductFilterValue.objects.filter(
                product_id__in=affected_product_ids,
                filter_value__filter_id=filter_obj.id,
            ).delete()

            category_filter.delete()
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return DisableCategoryFilterResponseDTO(
            category_id=category_obj.id,
            filter_id=filter_obj.id,
            affected_products_count=len(affected_product_ids),
        )

    def _find_category(self, category_id: int) -> Category:
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist as e:
            raise CategoryNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _find_filter(self, filter_id: int) -> Filter:
        try:
            return Filter.objects.get(id=filter_id)
        except Filter.DoesNotExist as e:
            raise FilterNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _find_category_filter(self, category_id: int, filter_id: int) -> CategoryFilter:
        try:
            return CategoryFilter.objects.get(category_id=category_id, filter_id=filter_id)
        except CategoryFilter.DoesNotExist as e:
            raise CategoryFilterNotAssociatedException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)