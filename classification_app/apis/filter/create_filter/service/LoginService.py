from django.db import OperationalError

from classification_app.apis.filter.create_filter.dtos import CreateFilterResponseDTO
from classification_app.apis.filter.create_filter.exception import FilterNameAlreadyExistsException
from classification_app.models import Filter
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from django.db import IntegrityError
from core.utils import build_unique_slug


class CreateFilterService:
    def execute(self, name: str, description: str) -> CreateFilterResponseDTO:
        slug = build_unique_slug(name)

        filter_obj: Filter = self._create_filter(name, description, slug)

        return CreateFilterResponseDTO(
            id=filter_obj.id,
            name=filter_obj.name,
            description=filter_obj.description,
            createdAt=filter_obj.created_at,
            slug=filter_obj.slug,
            isActive=filter_obj.is_active,
        )
    

    def _create_filter(self, name: str, description: str, slug: str) -> Filter:
        try:
            return Filter.objects.create(
                name=name,
                description=description,
                slug=slug,
            )
        except IntegrityError as e:
            raise FilterNameAlreadyExistsException(message="A filter with this name already exists.",cause=e,)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.",cause=e,)
        except Exception as e:
            raise InternalServerErrorException(
                message="Internal server error.",
                cause=e,
            )
        
