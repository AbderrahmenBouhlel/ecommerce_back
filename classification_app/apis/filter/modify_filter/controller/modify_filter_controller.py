from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter.modify_filter.dtos import ModifyFilterRequestDTO
from classification_app.apis.filter.modify_filter.mapper import ModifyFilterErrorMapper
from classification_app.apis.filter.modify_filter.service import ModifyFilterService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def modify_filter_controller(request, filter_id: int):
    """
    PATCH api/v1/admin/filters/{filterId}
    Updates name and/or description of a filter.
    """
    service = ModifyFilterService()

    try:
        request_dto = ModifyFilterRequestDTO.from_request(request=request, filter_id=filter_id)

        result_dto = service.execute(
            filter_id=request_dto.filter_id,
            name=request_dto.name,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.FILTER_UPDATED,
            message="Filter updated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ModifyFilterErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)