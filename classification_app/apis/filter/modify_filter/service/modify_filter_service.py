from django.db import IntegrityError, OperationalError, transaction
from django.utils import timezone

from classification_app.apis.filter.modify_filter.dtos import ModifyFilterResponseDTO
from classification_app.apis.filter.modify_filter.exception import FilterAlreadyExistsException
from classification_app.errors import FilterNotFoundException
from classification_app.models import Filter
from core.utils import build_unique_slug
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException


class ModifyFilterService:
    @transaction.atomic
    def execute(self, filter_id: int, name: str | None, description: str | None) -> ModifyFilterResponseDTO:
        filter_obj = self._find_filter(filter_id)

        should_update_name = name is not None and name != filter_obj.name
        should_update_description = description is not None and description != filter_obj.description

        if not should_update_name and not should_update_description:
            return ModifyFilterResponseDTO(
                id=filter_obj.id,
                name=filter_obj.name,
                slug=filter_obj.slug,
                description=filter_obj.description,
                is_active=filter_obj.is_active,
                updated_at=timezone.now(),
            )

        try:
            if should_update_name:
                filter_obj.name = name
                filter_obj.slug = build_unique_slug(name)

            if should_update_description:
                filter_obj.description = description

            update_fields = ["name", "slug", "description"]
            if not should_update_name:
                update_fields.remove("name")
                update_fields.remove("slug")
            if not should_update_description:
                update_fields.remove("description")

            filter_obj.save(update_fields=update_fields)
        except IntegrityError as e:
            raise FilterAlreadyExistsException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

        return ModifyFilterResponseDTO(
            id=filter_obj.id,
            name=filter_obj.name,
            slug=filter_obj.slug,
            description=filter_obj.description,
            is_active=filter_obj.is_active,
            updated_at=timezone.now(),
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