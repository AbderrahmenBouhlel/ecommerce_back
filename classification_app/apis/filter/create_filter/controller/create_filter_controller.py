from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.create_filter.dtos import CreateFilterRequestDTO
from classification_app.apis.filter.create_filter.mapper import CreateFilterErrorMapper
from classification_app.apis.filter.create_filter.service import CreateFilterService
from classification_app.apis.filter.get_all_filters.controller import get_all_filters_controller
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["GET", "POST"])
def create_filter_controller(request):
    """
    POST api/v1/admin/filters: Creates a new filter.
    GET api/v1/admin/filters: Returns all filters and their values.
    """
    if request.method == "GET":
        return get_all_filters_controller(request)

    service = CreateFilterService()

    try:
        request_dto = CreateFilterRequestDTO.from_request(request)

        result_dto = service.execute(
            name=request_dto.name,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.FILTER_CREATED,
            message="Filter created successfully.",
            data=result_dto,
            status=201,
        )

    except Exception as e:
        response = CreateFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)