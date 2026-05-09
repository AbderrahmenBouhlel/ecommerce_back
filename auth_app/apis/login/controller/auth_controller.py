
from auth_app.apis.login.service import LoginService
from core.apiResponse.response import ApiResponse , ApiCode
from auth_app.apis.login.mapper import LoginErrorMapper
from django.http import JsonResponse 
from auth_app.apis.login.dtos import LoginRequestDTO
from core.decorators import public_endpoint
from django.views.decorators.http import require_POST



@public_endpoint
@require_POST
def login_controller(request):
    """
    POST api/v1/auth/sessions
    The Entry Point for User Authentication.
    """
    
    service = LoginService()
    try:
        
       
        # 1. Extract Data (Request DTO equivalent)
        request_dto = LoginRequestDTO.from_request(request)
        
        # 2. Execute Business Logic (The Happy Path)
        # The Service returns a LoginResponseDTO
        
        result_dto = service.execute(email=request_dto.email, password=request_dto.password)

        
        # 3. Wrap in Success Envelope
        response = ApiResponse(
            code=ApiCode.AUTH_LOGIN_SUCCESS,
            message="Login completed successfully.", 
            data=result_dto,
            status=200
        )

    except Exception as e:
        # 4. Translate Error (The Sad Path)
        # The Mapper returns a pre-configured ApiResponse with the right status
        response = LoginErrorMapper.map(e)

    return JsonResponse(response.to_dict(), status=response.status)