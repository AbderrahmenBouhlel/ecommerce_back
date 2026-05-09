from django.http import JsonResponse
from django.views.decorators.http import require_POST

from classification_app.apis.filter_value.create_filter_value.dtos import CreateFilterValueRequestDTO
from classification_app.apis.filter_value.create_filter_value.mapper import CreateFilterValueErrorMapper
from classification_app.apis.filter_value.create_filter_value.service import CreateFilterValueService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_POST
def create_filter_value_controller(request, filter_id: int):
    """
    POST api/v1/admin/filters/{filterId}/values
    Creates a new value under a specific filter.
    """
    service = CreateFilterValueService()

    try:
        request_dto = CreateFilterValueRequestDTO.from_request(request)

        result_dto = service.execute(
            filter_id=filter_id,
            name=request_dto.name,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.FILTER_VALUE_CREATED,
            message="Filter value created successfully.",
            data=result_dto,
            status=201,
        )

    except Exception as e:
        response = CreateFilterValueErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
