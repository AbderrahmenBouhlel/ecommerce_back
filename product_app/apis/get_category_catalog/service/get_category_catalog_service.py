from django.db import OperationalError

from classification_app.errors import CategoryNotFoundException
from classification_app.models import Category, FilterValue
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from product_app.apis.get_category_catalog.dtos import (
    CategoryCatalogFilterValueDTO,
    CategoryCatalogProductDTO,
    GetCategoryCatalogRequestDTO,
    GetCategoryCatalogResponseDTO,
)
from product_app.errors import CategoryInactiveException
from product_app.models import Product, ProductFilterValue


class GetCategoryCatalogService:
    def execute(self, request_dto: GetCategoryCatalogRequestDTO) -> GetCategoryCatalogResponseDTO:
        category_obj = self._find_category_by_slug(request_dto.category_slug)
        products = self._find_active_products(category_obj.id)

        product_ids = [product_obj.id for product_obj in products]
        product_filter_values_map = self._get_product_filter_values_map(product_ids)
        used_filter_value_ids = self._find_used_filter_value_ids(product_ids)
        used_filter_values = self._find_used_filter_values(used_filter_value_ids)

        product_items = [
            CategoryCatalogProductDTO(
                id=product_obj.id,
                name=product_obj.name,
                slug=product_obj.slug,
                price=product_obj.price,
                cover_image_url=product_obj.cover_image_url,
                hover_image_url=product_obj.hover_image_url,
                is_active=(product_obj.status == "ACTIVE"),
                filter_values=product_filter_values_map.get(product_obj.id, []),
            )
            for product_obj in products
        ]

        filter_value_items = [
            CategoryCatalogFilterValueDTO(
                id=filter_value.id,
                name=filter_value.name,
                slug=filter_value.slug,
            )
            for filter_value in used_filter_values
        ]

        return GetCategoryCatalogResponseDTO(
            products=product_items,
            filter_values=filter_value_items,
        )

    def _find_category_by_slug(self, category_slug: str) -> Category:
        try:
            category_obj = Category.objects.get(slug=category_slug)

            if not category_obj.is_active:
                raise CategoryInactiveException(message="The specified category is inactive.")

            return category_obj
        except Category.DoesNotExist as e:
            raise CategoryNotFoundException(cause=e)
        except CategoryInactiveException:
            raise
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _find_active_products(self, category_id: int):
        try:
            return Product.objects.filter(category_id=category_id, status="ACTIVE").order_by("id")
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _get_product_filter_values_map(self, product_ids: list[int]) -> dict[int, list[CategoryCatalogFilterValueDTO]]:
        if not product_ids:
            return {}

        try:
            product_filter_values = ProductFilterValue.objects.filter(
                product_id__in=product_ids
            ).select_related("filter_value").order_by("product_id", "filter_value_id")

            product_map = {}
            for pf in product_filter_values:
                if pf.product_id not in product_map:
                    product_map[pf.product_id] = []
                product_map[pf.product_id].append(
                    CategoryCatalogFilterValueDTO(
                        id=pf.filter_value.id,
                        name=pf.filter_value.name,
                        slug=pf.filter_value.slug,
                    )
                )
            return product_map
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _find_used_filter_value_ids(self, product_ids: list[int]) -> list[int]:
        if not product_ids:
            return []

        try:
            return list(
                ProductFilterValue.objects.filter(product_id__in=product_ids)
                .values_list("filter_value_id", flat=True)
                .distinct()
            )
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _find_used_filter_values(self, filter_value_ids: list[int]):
        if not filter_value_ids:
            return []

        try:
            return (
                FilterValue.objects.filter(id__in=filter_value_ids)
                .order_by("id")
            )
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
