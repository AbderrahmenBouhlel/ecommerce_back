from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required
from product_app.apis.add_skus_for_variant.dtos import AddSkusForVariantRequestDTO
from product_app.apis.add_skus_for_variant.mapper import AddSkusForVariantErrorMapper
from product_app.apis.add_skus_for_variant.service import AddSkusForVariantService


@admin_required
@require_POST
def add_skus_for_variant_controller(request, variant_id):
    """
    POST /api/v1/admin/variants/{variant_id}/skus
    Add one or more SKUs (size/stock) to a specific variant.
    """
    service = AddSkusForVariantService()

    try:
        request_dto = AddSkusForVariantRequestDTO.from_request(request, variant_id)

        result_dto = service.execute(request_dto)

        response = ApiResponse(
            code=ApiCode.SKU_CREATED,
            message="SKUs successfully added to the variant.",
            data=result_dto,
            status=201,
        )
    except Exception as e:
        response = AddSkusForVariantErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
