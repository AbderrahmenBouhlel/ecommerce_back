from django.http import JsonResponse
from django.views.decorators.http import require_GET

from classification_app.apis.filter.get_all_filters.mapper import GetAllFiltersErrorMapper
from classification_app.apis.filter.get_all_filters.service import GetAllFiltersService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_GET
def get_all_filters_controller(request):
    """
    GET api/v1/admin/filters
    Returns all filters and their values.
    """
    service = GetAllFiltersService()

    try:
        result_dto = service.execute()

        response = ApiResponse(
            code=ApiCode.FILTERS_RETRIEVED,
            message="Filters retrieved successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = GetAllFiltersErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
