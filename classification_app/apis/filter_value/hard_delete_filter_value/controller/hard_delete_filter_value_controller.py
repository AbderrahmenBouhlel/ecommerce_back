from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter_value.hard_delete_filter_value.dtos import HardDeleteFilterValueRequestDTO
from classification_app.apis.filter_value.hard_delete_filter_value.mapper import HardDeleteFilterValueErrorMapper
from classification_app.apis.filter_value.hard_delete_filter_value.service import HardDeleteFilterValueService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["DELETE"])
def hard_delete_filter_value_controller(request, filter_value_id: int):
    """
    DELETE api/v1/admin/filter-values/{filterValueId}?confirm=true
    Hard deletes a filter value and related rows.
    """
    service = HardDeleteFilterValueService()

    try:
        request_dto = HardDeleteFilterValueRequestDTO.from_request(
            request=request,
            filter_value_id=filter_value_id,
        )

        result_dto = service.execute(filter_value_id=request_dto.filter_value_id)

        response = ApiResponse(
            code=ApiCode.FILTER_VALUE_HARD_DELETED,
            message="Filter value deleted successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = HardDeleteFilterValueErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
