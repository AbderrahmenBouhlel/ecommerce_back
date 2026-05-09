from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter_value.reactivate_filter_value.dtos import ReactivateFilterValueRequestDTO
from classification_app.apis.filter_value.reactivate_filter_value.mapper import ReactivateFilterValueErrorMapper
from classification_app.apis.filter_value.reactivate_filter_value.service import ReactivateFilterValueService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def reactivate_filter_value_controller(request, filter_value_id: int):
    """
    PATCH api/v1/admin/filter-values/{filterValueId}/activate
    Marks a filter value as active.
    """
    service = ReactivateFilterValueService()

    try:
        request_dto = ReactivateFilterValueRequestDTO.from_request(filter_value_id=filter_value_id)

        result_dto = service.execute(filter_value_id=request_dto.filter_value_id)

        response = ApiResponse(
            code=ApiCode.FILTER_VALUE_ACTIVATED,
            message="Filter value activated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ReactivateFilterValueErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)