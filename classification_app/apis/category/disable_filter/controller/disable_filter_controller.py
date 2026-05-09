from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.category.disable_filter.dtos import DisableCategoryFilterRequestDTO
from classification_app.apis.category.disable_filter.mapper import DisableCategoryFilterErrorMapper
from classification_app.apis.category.disable_filter.service import DisableCategoryFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["DELETE"])
def disable_filter_controller(request, category_id: int, filter_id: int):
    """
    DELETE api/v1/admin/categories/{categoryId}/filters/{filterId}
    Removes a filter from a category and deletes affected product-filter-value associations.
    """
    service = DisableCategoryFilterService()

    try:
        request_dto = DisableCategoryFilterRequestDTO.from_request(
            category_id=category_id,
            filter_id=filter_id,
        )

        result_dto = service.execute(
            category_id=request_dto.category_id,
            filter_id=request_dto.filter_id,
        )

        response = ApiResponse(
            code=ApiCode.CATEGORY_FILTER_REMOVED,
            message="Filter removed from category successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = DisableCategoryFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)