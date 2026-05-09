from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required
from product_app.apis.add_filter_values_for_product.dtos import AddFilterValuesForProductRequestDTO
from product_app.apis.add_filter_values_for_product.mapper import AddFilterValuesForProductErrorMapper
from product_app.apis.add_filter_values_for_product.service import AddFilterValuesForProductService


@admin_required
@require_POST
def add_filter_values_for_product_controller(request, product_id):
    """
    POST /api/v1/admin/products/{product_id}/filter-values
    Assign one or more filter values to a specific product.
    """
    service = AddFilterValuesForProductService()

    try:
        request_dto = AddFilterValuesForProductRequestDTO.from_request(request, product_id)

        result_dto = service.execute(request_dto)

        response = ApiResponse(
            code=ApiCode.PRODUCT_FILTER_VALUES_ASSIGNED,
            message="Filter values successfully assigned to the product.",
            data=result_dto,
            status=201,
        )
    except Exception as e:
        response = AddFilterValuesForProductErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
