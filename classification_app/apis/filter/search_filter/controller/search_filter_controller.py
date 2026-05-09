from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.search_filter.dtos import SearchFilterRequestDTO
from classification_app.apis.filter.search_filter.mapper import SearchFilterErrorMapper
from classification_app.apis.filter.search_filter.service import SearchFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["POST"])
def search_filter_controller(request):
    """
    POST api/v1/admin/filters/search
    Returns available filters for category assignment.
    """
    service = SearchFilterService()

    try:
        request_dto = SearchFilterRequestDTO.from_request(request)

        result_dto = service.execute(
            q=request_dto.q,
            excluded_ids=request_dto.excluded_ids,
        )

        response = ApiResponse(
            code=ApiCode.FILTERS_SEARCH_RESULTS,
            message="Available filters retrieved.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = SearchFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)