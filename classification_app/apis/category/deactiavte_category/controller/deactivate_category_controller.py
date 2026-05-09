from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.category.deactiavte_category.dtos import DeactivateCategoryRequestDTO
from classification_app.apis.category.deactiavte_category.mapper import DeactivateCategoryErrorMapper
from classification_app.apis.category.deactiavte_category.service import DeactivateCategoryService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def deactivate_category_controller(request, category_id: int):
    """
    PATCH api/v1/admin/categories/{categoryId}/deactivate
    Marks a category as inactive only.
    """
    service = DeactivateCategoryService()

    try:
        request_dto = DeactivateCategoryRequestDTO.from_request(category_id=category_id)

        result_dto = service.execute(category_id=request_dto.category_id)

        response = ApiResponse(
            code=ApiCode.CATEGORY_DEACTIVATED,
            message="Category deactivated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = DeactivateCategoryErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)