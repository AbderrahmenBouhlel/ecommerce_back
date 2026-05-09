
from django.urls import resolve
from django.http import JsonResponse
from core.apiResponse.response import ApiCode, ApiResponse
from auth_app.models import User


class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            view_func = resolve(request.path_info).func
        except Exception:
            return self.get_response(request)

        required_role = getattr(view_func, "required_role", None)
        is_public = getattr(view_func, "is_public", False)

        # No RBAC restriction
        if not required_role or is_public:
            return self.get_response(request)

        user: User = getattr(request, "user", None)

        if not user:
            return self._deny()

        if user.role != required_role:
            return self._deny()

        return self.get_response(request)

    def _deny(self):
        apiResponse = ApiResponse(
            code=ApiCode.AUTH_UNAUTHORIZED_ACTION,
            message="You are not allowed to perform this action.",
            status=403
        )
        return JsonResponse(apiResponse.to_dict(), status=403)