from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required
from product_app.apis.create_product.dtos import CreateProductRequestDTO
from product_app.apis.create_product.mapper import CreateProductErrorMapper
from product_app.apis.create_product.service import CreateProductService


@admin_required
@require_POST
def create_product_controller(request):
    """
    POST api/v1/admin/products
    Creates a new draft product.
    """
    service = CreateProductService()

    try:
        request_dto = CreateProductRequestDTO.from_request(request)

        result_dto = service.execute(
            name=request_dto.name,
            description=request_dto.description,
            price=request_dto.price,
            category_id=request_dto.category_id,
        )

        response = ApiResponse(
            code=ApiCode.PRODUCT_CREATED,
            message="Draft product created successfully.",
            data=result_dto,
            status=201,
        )
    except Exception as e:
        response = CreateProductErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)