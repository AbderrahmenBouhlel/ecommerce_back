from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from classification_app.apis.filter_value.modify_filter_value.dtos import ModifyFilterValueRequestDTO
from classification_app.apis.filter_value.modify_filter_value.mapper import ModifyFilterValueErrorMapper
from classification_app.apis.filter_value.modify_filter_value.service import ModifyFilterValueService
from core.apiResponse.response import ApiCode, ApiResponse
from core.decorators import admin_required


@admin_required
@require_http_methods(["PATCH"])
def modify_filter_value_controller(request, filter_value_id: int):
    """
    PATCH api/v1/admin/filter-values/{filterValueId}
    Updates name and/or description of a filter value.
    """
    service = ModifyFilterValueService()

    try:
        request_dto = ModifyFilterValueRequestDTO.from_request(request=request, filter_value_id=filter_value_id)

        result_dto = service.execute(
            filter_value_id=request_dto.filter_value_id,
            name=request_dto.name,
            description=request_dto.description,
        )

        response = ApiResponse(
            code=ApiCode.FILTER_VALUE_UPDATED,
            message="Filter value updated successfully.",
            data=result_dto,
            status=200,
        )

    except Exception as e:
        response = ModifyFilterValueErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)