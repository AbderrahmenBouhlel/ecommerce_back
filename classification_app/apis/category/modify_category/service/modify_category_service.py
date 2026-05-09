from django.db import IntegrityError, OperationalError, transaction
from django.utils import timezone

from classification_app.apis.category.modify_category.dtos import ModifyCategoryResponseDTO
from classification_app.apis.category.modify_category.exception import CategoryAlreadyExistsException
from classification_app.errors import CategoryNotFoundException
from classification_app.models import Category
from core.utils import build_unique_slug
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class ModifyCategoryService:
    @transaction.atomic
    def execute(self, category_id: int, name: str | None, description: str | None) -> ModifyCategoryResponseDTO:
        category_obj = self._find_category(category_id)

        should_update_name = name is not None and name != category_obj.name
        should_update_description = description is not None and description != category_obj.description

        if not should_update_name and not should_update_description:
            return ModifyCategoryResponseDTO(
                id=category_obj.id,
                name=category_obj.name,
                gender=category_obj.gender,
                slug=category_obj.slug,
                description=category_obj.description,
                is_active=category_obj.is_active,
                created_at=category_obj.created_at,
                updated_at=timezone.now(),
            )

        try:
            if should_update_name:
                category_obj.name = name
                category_obj.slug = build_unique_slug(f"{name}-{category_obj.gender}")

            if should_update_description:
                category_obj.description = description

            update_fields = ["name", "slug", "description"]
            if not should_update_name:
                update_fields.remove("name")
                update_fields.remove("slug")
            if not should_update_description:
                update_fields.remove("description")

            category_obj.save(update_fields=update_fields)
        except IntegrityError as e:
            raise CategoryAlreadyExistsException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ModifyCategoryResponseDTO(
            id=category_obj.id,
            name=category_obj.name,
            gender=category_obj.gender,
            slug=category_obj.slug,
            description=category_obj.description,
            is_active=category_obj.is_active,
            created_at=category_obj.created_at,
            updated_at=timezone.now(),
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