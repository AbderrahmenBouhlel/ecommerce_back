from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter_value.deactivate_filter_value.dtos import DeactivateFilterValueRequestDTO
from classification_app.apis.filter_value.deactivate_filter_value.mapper import DeactivateFilterValueErrorMapper
from classification_app.apis.filter_value.deactivate_filter_value.service import DeactivateFilterValueService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def deactivate_filter_value_controller(request, filter_value_id: int):
    """
    PATCH api/v1/admin/filter-values/{filterValueId}/deactivate
    Marks a filter value as inactive.
    """
    service = DeactivateFilterValueService()

    try:
        request_dto = DeactivateFilterValueRequestDTO.from_request(filter_value_id=filter_value_id)

        result_dto = service.execute(filter_value_id=request_dto.filter_value_id)

        response = ApiResponse(
            code=ApiCode.FILTER_VALUE_DEACTIVATED,
            message="Filter value deactivated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = DeactivateFilterValueErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)