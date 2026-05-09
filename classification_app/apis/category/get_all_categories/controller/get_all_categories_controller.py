from django.http import JsonResponse
from django.views.decorators.http import require_GET

from classification_app.apis.category.get_all_categories.mapper import GetAllCategoriesErrorMapper
from classification_app.apis.category.get_all_categories.service import GetAllCategoriesService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_GET
def get_all_categories_controller(request):
    """
    GET api/v1/admin/categories
    Returns all categories and their allowed filters.
    """
    service = GetAllCategoriesService()

    try:
        result_dto = service.execute()

        response = ApiResponse(
            code=ApiCode.CATEGORIES_RETRIEVED,
            message="Categories and their allowed filters retrieved successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = GetAllCategoriesErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)