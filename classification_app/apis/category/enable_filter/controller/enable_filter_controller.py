from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.category.enable_filter.dtos import EnableCategoryFilterRequestDTO
from classification_app.apis.category.enable_filter.mapper import EnableCategoryFilterErrorMapper
from classification_app.apis.category.enable_filter.service import EnableCategoryFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["POST"])
def enable_filter_controller(request, category_id: int, filter_id: int):
    """
    POST api/v1/admin/categories/{categoryId}/filters/{filterId}
    Enables a filter for a category.
    """
    service = EnableCategoryFilterService()

    try:
        request_dto = EnableCategoryFilterRequestDTO.from_request(
            category_id=category_id,
            filter_id=filter_id,
        )

        result_dto = service.execute(
            category_id=request_dto.category_id,
            filter_id=request_dto.filter_id,
        )

        response = ApiResponse(
            code=ApiCode.CATEGORY_FILTER_ENABLED,
            message="Filter enabled for category successfully.",
            data=result_dto,
            status=201,
        )

    except Exception as e:
        response = EnableCategoryFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)