from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.category.modify_category.dtos import ModifyCategoryRequestDTO
from classification_app.apis.category.modify_category.mapper import ModifyCategoryErrorMapper
from classification_app.apis.category.modify_category.service import ModifyCategoryService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def modify_category_controller(request, category_id: int):
    """
    PATCH api/v1/admin/categories/{categoryId}
    Updates name and/or description of a category.
    """
    service = ModifyCategoryService()

    try:
        request_dto = ModifyCategoryRequestDTO.from_request(request=request, category_id=category_id)

        result_dto = service.execute(
            category_id=request_dto.category_id,
            name=request_dto.name,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.CATEGORY_UPDATED,
            message="Category updated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ModifyCategoryErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)