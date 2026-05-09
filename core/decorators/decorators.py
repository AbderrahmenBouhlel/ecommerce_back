




def public_endpoint(view_func):
    view_func.is_public = True
    return view_func




def admin_required(view_func):
    view_func.required_role = "ADMIN"
    view_func.is_public = False
    return view_func