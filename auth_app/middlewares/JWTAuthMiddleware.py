import jwt
from auth_app.services.jwt import JWTService, JWTPayload
from auth_app.models import User
from auth_app.repos.UserRespository import user_repository
from django.http import JsonResponse
from config import settings
from core.apiResponse.response import ApiResponse,ApiCode
from core.exceptions.excecptions import ServerUnavailableException
from typing import  Generic, TypeVar
from django.urls import resolve


D = TypeVar('D')
E = TypeVar('E')

class Result(Generic[D, E]):
    def __init__(self, success: bool, data: D = None, error: E = None):
        self.success = success
        self.data = data
        self.error = error



class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
         # Skip media files
        if request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)
        
        try:
            match = resolve(request.path_info)
            view_func = match.func
            
            # ignore authentication for public endpoints
            if getattr(view_func, 'is_public', False):
                return self.get_response(request)
        except Exception as e:
            pass
        
    
        
        token = request.headers.get("Authorization", "").replace("Bearer", "").strip()
        
        #1 Validate token existence
        token_exist_result: Result[None, ApiResponse] = self.assert_token_exists(token)
        if not token_exist_result.success:
            return self.build_http_response(token_exist_result.error)

        #2 Decode JWT and validate
        jwt_result: Result[JWTPayload, ApiResponse] = self.decode_jwt(token)
        if not jwt_result.success:
            return self.build_http_response(jwt_result.error)

        jwt_payload: JWTPayload = jwt_result.data

        #3 find user record from DB and validate
        user_result: Result[User, ApiResponse] = self.find_user(jwt_payload.id)
        if not user_result.success:
            return self.build_http_response(user_result.error)
        
        user: User = user_result.data
        
        #4 assert user is active
        active_result: Result[None, ApiResponse] = self.assert_user_is_active(user)
        if not active_result.success:
            return self.build_http_response(active_result.error)
        
        
        #5 attach user to request and proceed
        request.user = user
        response = self.get_response(request)
        
        return response
    
    
 
    def build_http_response(self, api_response: ApiResponse):
        return JsonResponse(api_response.to_dict(), status=api_response.status)
    
    
    
    
    
    def assert_token_exists(self, token: str) -> Result[None, ApiResponse]:
        if not token:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.AUTH_MISSING_TOKEN,
                message="Authentication token is required.",
                status=401
            ))
        return Result(success=True)
    
    
    def decode_jwt(self, token: str) -> Result[JWTPayload, ApiResponse]:
        try :
            jwt_payload : JWTPayload = JWTService.decode(token) 
            return Result(success=True, data=jwt_payload)
        except jwt.ExpiredSignatureError as e:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.AUTH_EXPIRED_TOKEN,
                message="Authentication token has expired.",
                status=401
            ))
        except jwt.InvalidTokenError as e:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.AUTH_INVALID_TOKEN,
                message="Invalid authentication token.",
                status=401
            ))
        except Exception as e:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.SYSTEM_INTERNAL_ERROR,
                message="Internal server error.",
                status=500
            ))
    
    
    def find_user(self, user_id: int) -> Result[User, ApiResponse]:
        try:
            user = user_repository.find_by_id(user_id)
            return Result(success=True, data=user)
        except User.DoesNotExist:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.AUTH_INVALID_TOKEN,
                message="Invalid authentication token.",
                status=401
            ))
        except ServerUnavailableException:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.SYSTEM_SERVICE_UNAVAILABLE,
                message="Service temporarily unavailable.",
                status=503
            ))
        except Exception as e:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.SYSTEM_INTERNAL_ERROR,
                message="Internal server error.",
                status=500
            ))
            
    def assert_user_is_active(self, user: User) -> Result[None, ApiResponse]:
        if not user.is_active:
            return Result(success=False, error=ApiResponse(
                code=ApiCode.AUTH_USER_INACTIVE,
                message="Access denied.",
                status=403
            ))
        return Result(success=True)
