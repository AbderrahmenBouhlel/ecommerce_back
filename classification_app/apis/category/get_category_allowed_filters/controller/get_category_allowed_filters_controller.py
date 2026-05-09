from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.decorators import admin_required
from core.apiResponse.response import ApiResponse, ApiCode
from classification_app.apis.category.get_category_allowed_filters.service import GetCategoryAllowedFiltersService
from classification_app.apis.category.get_category_allowed_filters.mapper import GetCategoryAllowedFiltersErrorMapper


@admin_required
@require_GET
def get_category_allowed_filters_controller(request, category_id):
    """
    GET /api/v1/admin/categories/{category_id}/filters
    Retrieve all filters assigned to a category along with their allowed filter values.
    """
    service = GetCategoryAllowedFiltersService()

    try:
        result_dto = service.execute(category_id)

        response = ApiResponse(
            code=ApiCode.CATEGORIES_FILTERS_RETRIEVED,
            message="Category filters retrieved successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = GetCategoryAllowedFiltersErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
