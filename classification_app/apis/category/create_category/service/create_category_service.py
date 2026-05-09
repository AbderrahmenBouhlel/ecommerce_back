from django.db import IntegrityError, OperationalError

from classification_app.apis.category.create_category.dtos import CreateCategoryResponseDTO
from classification_app.apis.category.create_category.exception import CategoryNameAlreadyExistsException
from classification_app.models import Category
from core.utils import build_unique_slug
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class CreateCategoryService:
    def execute(self, name: str, gender: str, description: str) -> CreateCategoryResponseDTO:
        slug = build_unique_slug(f"{name}-{gender}")
        category_obj: Category = self._create_category(name, gender, slug, description)

        return CreateCategoryResponseDTO(
            id=category_obj.id,
            name=category_obj.name,
            gender=category_obj.gender,
            slug=category_obj.slug,
            description=category_obj.description,
            is_active=category_obj.is_active,
            created_at=category_obj.created_at,
        )

    def _create_category(self, name: str, gender: str, slug: str, description: str) -> Category:
        try:
            return Category.objects.create(
                name=name,
                gender=gender,
                slug=slug,
                description=description,
            )
        except IntegrityError as e:
            raise CategoryNameAlreadyExistsException(
                message="A category with this name already exists for this gender.",
                cause=e,
            )
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(
                message="Internal server error.",
                cause=e,
            )