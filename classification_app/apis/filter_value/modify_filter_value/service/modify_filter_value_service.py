from django.db import IntegrityError, OperationalError, transaction
from django.utils import timezone

from classification_app.apis.filter_value.modify_filter_value.dtos import ModifyFilterValueResponseDTO
from classification_app.apis.filter_value.modify_filter_value.exception import FilterValueAlreadyExistsException
from classification_app.errors import FilterNotFoundException
from classification_app.models import FilterValue
from core.utils import build_unique_slug
from core.exceptions.excecptions import InternalServerErrorException, RequestValidationException, ServerUnavailableException


class ModifyFilterValueService:
    @transaction.atomic
    def execute(self, filter_value_id: int, name: str | None, description: str | None) -> ModifyFilterValueResponseDTO:
        filter_value = self._find_filter_value(filter_value_id)

        should_update_name = name is not None and name != filter_value.name
        should_update_description = description is not None and description != filter_value.description

        if not should_update_name and not should_update_description:
            raise RequestValidationException(message="Invalid request. dues to missing or invalid parameters.", cause=None)

        try:
            
            update_fields = []
            if should_update_name:
                filter_value.name = name
                filter_value.slug = build_unique_slug(name)
                update_fields.extend(["name", "slug"])
                
            if should_update_description:
                filter_value.description = description
                update_fields.append("description")

            filter_value.save(update_fields=update_fields)
        except IntegrityError as e:
            raise FilterValueAlreadyExistsException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ModifyFilterValueResponseDTO(
            id=filter_value.id,
            filter_id=filter_value.filter_id,
            name=filter_value.name,
            slug=filter_value.slug,
            description=filter_value.description,
            is_active=filter_value.is_active,
            updated_at=timezone.now(),
        )

    def _find_filter_value(self, filter_value_id: int) -> FilterValue:
        try:
            return FilterValue.objects.get(id=filter_value_id)
        except FilterValue.DoesNotExist as e:
            raise FilterNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
