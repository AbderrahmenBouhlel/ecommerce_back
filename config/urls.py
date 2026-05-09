"""
URL configuration for EcommerceProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static



from django.urls import path
from auth_app.apis.login.controller import login_controller
from auth_app.apis.signup.controller import signup_controller
from auth_app.apis.me.controller import me_controller

from classification_app.apis.category.get_all_categories_light.controller.get_all_categories_light_controller import get_all_categories_light_controller
from classification_app.apis.filter.create_filter.controller import create_filter_controller
from classification_app.apis.category.create_category.controller import create_category_controller
from classification_app.apis.category.activate_category.controller import activate_category_controller
from classification_app.apis.category.deactiavte_category.controller import deactivate_category_controller
from classification_app.apis.category.enable_filter.controller import enable_filter_controller
from classification_app.apis.category.disable_filter.controller import disable_filter_controller
from classification_app.apis.category.get_all_categories.controller import get_all_categories_controller
from classification_app.apis.category.modify_category.controller import modify_category_controller
from classification_app.apis.category.get_category_allowed_filters.controller import get_category_allowed_filters_controller


from classification_app.apis.filter.search_filter.controller import search_filter_controller
from classification_app.apis.filter.deactivate_filter.controller import deactivate_filter_controller
from classification_app.apis.filter.modify_filter.controller import modify_filter_controller
from classification_app.apis.filter.reactivate_filter.controller import reactivate_filter_controller
from classification_app.apis.filter.hard_delete_filter.controller.hard_delete_filter_controller import hard_delete_filter_controller
from classification_app.apis.filter.get_all_filters.controller import get_all_filters_controller

from classification_app.apis.filter_value.create_filter_value.controller import create_filter_value_controller
from classification_app.apis.filter_value.deactivate_filter_value.controller import deactivate_filter_value_controller
from classification_app.apis.filter_value.modify_filter_value.controller import modify_filter_value_controller
from classification_app.apis.filter_value.reactivate_filter_value.controller import reactivate_filter_value_controller
from classification_app.apis.filter_value.hard_delete_filter_value.controller import hard_delete_filter_value_controller



from product_app.routes.urls import urlpatterns as product_urls


urlpatterns = [
    
    # auth paths
    path('api/v1/auth/sessions', login_controller, name='login'),
    path('api/v1/auth/users', signup_controller, name='signup'),
    path('api/v1/auth/me', me_controller, name='me'),
   
    # category paths
    path('api/v1/admin/categories', get_all_categories_controller, name='get_all_categories'),
    path('api/v1/admin/categories/light', get_all_categories_light_controller, name='get_all_categories_light'),
    path('api/v1/admin/categories/create', create_category_controller, name='create_category'),
    path('api/v1/admin/categories/<int:category_id>', modify_category_controller, name='modify_category'),
    path('api/v1/admin/categories/<int:category_id>/activate', activate_category_controller, name='activate_category'),
    path('api/v1/admin/categories/<int:category_id>/deactivate', deactivate_category_controller, name='deactivate_category'),
    path('api/v1/admin/categories/<int:category_id>/filters/<int:filter_id>/enable', enable_filter_controller, name='enable_category_filter'),
    path('api/v1/admin/categories/<int:category_id>/filters/<int:filter_id>/disable', disable_filter_controller, name='disable_category_filter'),
    path('api/v1/admin/categories/<int:category_id>/filters', get_category_allowed_filters_controller, name='get_category_allowed_filters'),

    # filter value paths
    path('api/v1/admin/filters/<int:filter_id>/values', create_filter_value_controller, name='create_filter_value'),
    path('api/v1/admin/filter-values/<int:filter_value_id>', modify_filter_value_controller, name='modify_filter_value'),
    path('api/v1/admin/filter-values/<int:filter_value_id>/activate', reactivate_filter_value_controller, name='reactivate_filter_value'),
    path('api/v1/admin/filter-values/<int:filter_value_id>/deactivate', deactivate_filter_value_controller, name='deactivate_filter_value'),
    path('api/v1/admin/filter-values/<int:filter_value_id>/delete', hard_delete_filter_value_controller, name='hard_delete_filter_value'),

    # product paths
    path('', include(product_urls)),
    
    
    # filter paths
    path('api/v1/admin/filters', get_all_filters_controller, name='get_all_filters'),
    path('api/v1/admin/filters/search', search_filter_controller, name='search_filter'),
    path('api/v1/admin/filters/create', create_filter_controller, name='create_filter'),
    path('api/v1/admin/filters/<int:filter_id>', modify_filter_controller, name='modify_filter'),
    path('api/v1/admin/filters/<int:filter_id>/activate', reactivate_filter_controller, name='reactivate_filter'),
    path('api/v1/admin/filters/<int:filter_id>/deactivate', deactivate_filter_controller, name='deactivate_filter'),
    path('api/v1/admin/filters/<int:filter_id>', hard_delete_filter_controller, name='hard_delete_filter'),
    
    

  
]



# (Development Mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)