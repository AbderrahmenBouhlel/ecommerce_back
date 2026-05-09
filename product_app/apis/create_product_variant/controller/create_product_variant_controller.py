from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required
from product_app.apis.create_product_variant.dtos import CreateProductVariantRequestDTO
from product_app.apis.create_product_variant.mapper import CreateProductVariantErrorMapper
from product_app.apis.create_product_variant.service import CreateProductVariantService
from product_app.apis.create_product_variant.service.add_variant_images_service import AddVariantImagesService
from product_app.apis.create_product_variant.dtos import CreateProductVariantResponseDTO



@admin_required
@require_POST
def create_product_variant_controller(request, id):
    """
    POST api/v1/admin/products/{id}/variants
    Creates a new variant (color) for a specific product.
    """
    addVariantImagesService = AddVariantImagesService()
    service = CreateProductVariantService(addVariantImagesService=addVariantImagesService)



    try:
        request_dto = CreateProductVariantRequestDTO.from_request(request , id=id)
    
        result_dto: CreateProductVariantResponseDTO = service.execute(
            product_id=request_dto.id,
            color_name=request_dto.color_name,
            color_code=request_dto.color_code,
            images=request_dto.images
        )

        response = ApiResponse(
            code=ApiCode.VARIANT_CREATED,
            message="Product variant created successfully.",
            data=result_dto,
            status=201,
        )
    except Exception as e:
        response = CreateProductVariantErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)
