from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.reactivate_filter.dtos import ReactivateFilterRequestDTO
from classification_app.apis.filter.reactivate_filter.mapper import ReactivateFilterErrorMapper
from classification_app.apis.filter.reactivate_filter.service import ReactivateFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def reactivate_filter_controller(request, filter_id: int):
    """
    PATCH api/v1/admin/filters/{filterId}/activate
    Marks a filter as active only.
    """
    service = ReactivateFilterService()

    try:
        request_dto = ReactivateFilterRequestDTO.from_request(filter_id=filter_id)

        result_dto = service.execute(filter_id=request_dto.filter_id)

        response = ApiResponse(
            code=ApiCode.FILTER_ACTIVATED,
            message="Filter activated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ReactivateFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)