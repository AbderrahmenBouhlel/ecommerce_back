from django.db import IntegrityError, OperationalError, transaction

from classification_app.apis.category.enable_filter.dtos import EnableCategoryFilterResponseDTO
from classification_app.apis.category.enable_filter.exception import CategoryFilterAlreadyEnabledException
from classification_app.errors import CategoryNotFoundException, FilterNotFoundException
from classification_app.models import Category, CategoryFilter, Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class EnableCategoryFilterService:
    @transaction.atomic
    def execute(self, category_id: int, filter_id: int) -> EnableCategoryFilterResponseDTO:
        category_obj = self._find_category(category_id)
        filter_obj = self._find_filter(filter_id)

        try:
            CategoryFilter.objects.create(
                category=category_obj,
                filter=filter_obj,
            )
        except IntegrityError as e:
            raise CategoryFilterAlreadyEnabledException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return EnableCategoryFilterResponseDTO(
            category_id=category_obj.id,
            filter_id=filter_obj.id,
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