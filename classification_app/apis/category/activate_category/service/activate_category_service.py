from django.db import OperationalError, transaction

from classification_app.apis.category.activate_category.dtos import ActivateCategoryResponseDTO
from classification_app.apis.category.activate_category.exception import CategoryAlreadyActiveException
from classification_app.errors import CategoryNotFoundException
from classification_app.models import Category
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class ActivateCategoryService:
    @transaction.atomic
    def execute(self, category_id: int) -> ActivateCategoryResponseDTO:
        category_obj = self._find_category(category_id)

        if category_obj.is_active:
            raise CategoryAlreadyActiveException()

        try:
            category_obj.is_active = True
            category_obj.save(update_fields=["is_active"])
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ActivateCategoryResponseDTO(
            category_id=category_obj.id,
            is_active=category_obj.is_active,
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