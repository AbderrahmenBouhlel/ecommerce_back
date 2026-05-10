
from django.urls import path


from django.urls import path


from product_app.apis.create_product.controller import create_product_controller
from product_app.apis.create_product_variant.controller import create_product_variant_controller
from product_app.apis.get_category_catalog.controller import get_category_catalog_controller

from product_app.apis.add_skus_for_variant.controller.add_skus_for_variant_controller import add_skus_for_variant_controller
from product_app.apis.add_filter_values_for_product.controller import add_filter_values_for_product_controller
urlpatterns = [
    # product paths
    path('api/v1/admin/products', create_product_controller, name='create_product'),
    
    path('api/v1/admin/products/<int:id>/variants', create_product_variant_controller, name='create_product_variant'),
    path('api/v1/admin/variants/<int:variant_id>/skus', add_skus_for_variant_controller, name='add_skus_for_variant'),
    path('api/v1/admin/products/<int:product_id>/filter-values', add_filter_values_for_product_controller, name='add_filter_values_for_product'),
    path('api/v1/products/categories/<slug:category_slug>/catalog', get_category_catalog_controller, name='get_category_catalog'),
]

