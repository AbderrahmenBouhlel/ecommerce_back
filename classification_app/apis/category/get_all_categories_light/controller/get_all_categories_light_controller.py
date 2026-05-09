from django.http import JsonResponse
from django.views.decorators.http import require_GET

from classification_app.apis.category.get_all_categories_light.mapper import GetAllCategoriesSelectErrorMapper
from classification_app.apis.category.get_all_categories_light.service import GetAllCategoriesSelectService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import public_endpoint


@public_endpoint
@require_GET
def get_all_categories_light_controller(request):
    """
    GET api/v1/admin/categories/light
    Returns a lightweight list of categories for selection controls.
    """
    service = GetAllCategoriesSelectService()

    try:
        result_dto = service.execute()

        response = ApiResponse(
            code=ApiCode.CATEGORIES_SELECT_RETRIEVED,
            message="Categories retrieved successfully for selection.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = GetAllCategoriesSelectErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
