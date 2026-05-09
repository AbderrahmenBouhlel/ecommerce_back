from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.category.activate_category.dtos import ActivateCategoryRequestDTO
from classification_app.apis.category.activate_category.mapper import ActivateCategoryErrorMapper
from classification_app.apis.category.activate_category.service import ActivateCategoryService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def activate_category_controller(request, category_id: int):
    """
    PATCH api/v1/admin/categories/{categoryId}/activate
    Marks a category as active only.
    """
    service = ActivateCategoryService()

    try:
        request_dto = ActivateCategoryRequestDTO.from_request(category_id=category_id)

        result_dto = service.execute(category_id=request_dto.category_id)

        response = ApiResponse(
            code=ApiCode.CATEGORY_ACTIVATED,
            message="Category activated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ActivateCategoryErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)