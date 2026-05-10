from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import public_endpoint
from product_app.apis.get_category_catalog.dtos import GetCategoryCatalogRequestDTO
from product_app.apis.get_category_catalog.mapper import GetCategoryCatalogErrorMapper
from product_app.apis.get_category_catalog.service import GetCategoryCatalogService


@public_endpoint
@require_GET
def get_category_catalog_controller(request, category_slug: str):
    """
    GET /api/v1/products/categories/{category_slug}/catalog
    Retrieve category catalog by slug: active products and used filter values.
    """
    service = GetCategoryCatalogService()

    try:
        request_dto = GetCategoryCatalogRequestDTO.from_path(category_slug=category_slug)
        result_dto = service.execute(request_dto)

        response = ApiResponse(
            code=ApiCode.CATALOG_RETRIEVED,
            message="Category catalog retrieved successfully.",
            data=result_dto,
            status=200,
        )
    except Exception as e:
        response = GetCategoryCatalogErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
