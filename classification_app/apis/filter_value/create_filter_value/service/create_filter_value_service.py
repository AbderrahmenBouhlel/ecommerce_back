from django.db import IntegrityError, OperationalError

from classification_app.apis.filter_value.create_filter_value.dtos import CreateFilterValueResponseDTO
from classification_app.apis.filter_value.create_filter_value.exception import FilterValueAlreadyExistsException
from classification_app.errors import FilterNotFoundException
from classification_app.models import Filter, FilterValue
from core.exceptions.excecptions import InternalServerErrorException, RequestValidationException, ServerUnavailableException
from core.utils import build_unique_slug

class CreateFilterValueService:
    def execute(self, filter_id: int, name: str, description: str) -> CreateFilterValueResponseDTO:
        if filter_id <= 0:
            raise RequestValidationException(message="Invalid filter value request.", cause=None)


      
        filter_obj = self._find_filter(filter_id)   
        slug = build_unique_slug(name)
        
   
        filter_value = self._create_filter_value(
            filter_obj=filter_obj,
            name=name,
            slug=slug,
            description=description
        )

        return CreateFilterValueResponseDTO(
            id=filter_value.id,
            filter_id=filter_value.filter_id,
            name=filter_value.name,
            slug=filter_value.slug,
            is_active=filter_value.is_active,
            created_at=filter_value.created_at,
            description=filter_value.description,
        )

    def _find_filter(self, filter_id: int) -> Filter:
        try:
            return Filter.objects.get(id=filter_id)
        except Filter.DoesNotExist as e:
            raise FilterNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _create_filter_value(self, filter_obj: Filter, name: str, slug: str, description: str) -> FilterValue:
        try:
            return FilterValue.objects.create(
                filter=filter_obj,
                name=name,
                slug=slug,
                description=description
            )
        except IntegrityError as e:
            raise FilterValueAlreadyExistsException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
