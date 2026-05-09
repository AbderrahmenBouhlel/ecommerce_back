from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.deactivate_filter.dtos import DeactivateFilterRequestDTO
from classification_app.apis.filter.deactivate_filter.mapper import DeactivateFilterErrorMapper
from classification_app.apis.filter.deactivate_filter.service import DeactivateFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def deactivate_filter_controller(request, filter_id: int):
    """
    PATCH api/v1/admin/filters/{filterId}/deactivate
    Marks a filter and all its values as inactive.
    """
    service = DeactivateFilterService()

    try:
        request_dto = DeactivateFilterRequestDTO.from_request(filter_id=filter_id)

        result_dto = service.execute(filter_id=request_dto.filter_id)

        response = ApiResponse(
            code=ApiCode.FILTER_DEACTIVATED,
            message="Filter and its values deactivated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = DeactivateFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)