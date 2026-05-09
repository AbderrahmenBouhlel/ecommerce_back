from auth_app.apis.me.dtos.me_response import MeResponseDTO
from core.apiResponse.response import ApiResponse , ApiCode
from django.http import JsonResponse 
from core.decorators import public_endpoint
from django.views.decorators.http import require_GET
from auth_app.dtos import UserProfileDTO
from auth_app.models import User


@require_GET
def me_controller(request):
    """
    GET api/v1/auth/me
    Returns current authenticated user session.
    Middleware guarantees authentication.:
    """

    try:
        # 1. Extract authenticated user (already validated by middleware)
        user :User = request.user

        
        me_response_dto = MeResponseDTO(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role
        )


        print(me_response_dto.to_dict())
        # 3. Build success response
        response = ApiResponse(
            code=ApiCode.AUTH_SESSION_ACTIVE,
            message="Authenticated user session.",
            data=me_response_dto ,
            status=200
        )

    except Exception as e:
        # fallback only for unexpected server issues
        response = ApiResponse(
            code=ApiCode.SYSTEM_INTERNAL_ERROR,
            message="Internal server error.",
            status=500
        )

    return JsonResponse(response.to_dict(), status=response.status)