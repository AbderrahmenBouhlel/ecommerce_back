from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.hard_delete_filter.service.hard_delete_filter_service import HardDeleteFilterService
from classification_app.apis.filter.hard_delete_filter.dtos import HardDeleteFilterRequestDTO
from classification_app.apis.filter.hard_delete_filter.mapper import HardDeleteFilterErrorMapper

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["DELETE"])
def hard_delete_filter_controller(request, filter_id: int):
    """
    DELETE api/v1/admin/filters/{filterId}?confirm=true
    Hard deletes a filter and related rows.
    """
    service = HardDeleteFilterService()

    try:
        request_dto = HardDeleteFilterRequestDTO.from_request(
            request=request,
            filter_id=filter_id,
        )

        result_dto = service.execute(filter_id=request_dto.filter_id)

        response = ApiResponse(
            code=ApiCode.FILTER_HARD_DELETED,
            message="Filter and all related data deleted successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = HardDeleteFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
