from django.http import JsonResponse
from django.views.decorators.http import require_POST

from classification_app.apis.category.create_category.dtos import CreateCategoryRequestDTO
from classification_app.apis.category.create_category.mapper import CreateCategoryErrorMapper
from classification_app.apis.category.create_category.service import CreateCategoryService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_POST
def create_category_controller(request):
    """
    POST api/v1/admin/categories/create
    Creates a new category.
    """
    service = CreateCategoryService()

    try:
        request_dto = CreateCategoryRequestDTO.from_request(request)

        result_dto = service.execute(
            name=request_dto.name,
            gender=request_dto.gender,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.CATEGORY_CREATED,
            message="Category created successfully.",
            data=result_dto,
            status=201,
        )

    except Exception as e:
        response = CreateCategoryErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)