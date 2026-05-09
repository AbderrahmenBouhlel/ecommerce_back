from core.apiResponse.response import ApiResponse , ApiCode
from django.http import JsonResponse 
from core.decorators import public_endpoint
from django.views.decorators.http import require_POST




from core.apiResponse.response import ApiResponse, ApiCode
from auth_app.apis.signup.dtos import SignupRequestDTO
from auth_app.apis.signup.mapper.error_mapper import SignupErrorMapper
from auth_app.apis.signup.service.signup_service import SignupService


@public_endpoint
@require_POST
def signup_controller(request):
    """
    POST api/v1/auth/users
    Creates a customer account and returns a JWT token immediately.
    """
    service = SignupService()

    try:
        request_dto = SignupRequestDTO.from_request(request)

        result_dto = service.execute(
            email=request_dto.email,
            password=request_dto.password,
            name=request_dto.name,
        )

        response = ApiResponse(
            code=ApiCode.AUTH_SIGNUP_SUCCESS,
            message="Account created successfully.",
            data=result_dto,
            status=201,
        )

    except Exception as e:
        response = SignupErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)