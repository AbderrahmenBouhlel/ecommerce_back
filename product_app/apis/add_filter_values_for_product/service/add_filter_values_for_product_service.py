from typing import List

from django.db import transaction, OperationalError

from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from product_app.apis.add_filter_values_for_product.dtos import AddFilterValuesForProductResponseDTO, ProductFilterValueDTO
from product_app.apis.add_filter_values_for_product.dtos.add_filter_values_request import AddFilterValuesForProductRequestDTO
from product_app.models import Product, ProductFilterValue
from classification_app.models import FilterValue, CategoryFilter
from classification_app.errors import FilterValueNotFoundException
from product_app.errors import ProductNotFoundException
from product_app.apis.add_filter_values_for_product.exception.exception import FilterValueNotAllowedException
from core.services.embedding.EmbeddingService import EmbeddingService


class AddFilterValuesForProductService:
    @transaction.atomic
    def execute(self, request_dto: AddFilterValuesForProductRequestDTO) -> AddFilterValuesForProductResponseDTO:
        created_assignments: List[ProductFilterValue] = []

        try:
            product: Product = self.__find_product_and_lock(request_dto.product_id)

            for item in request_dto.filter_values:
                fv_id = item['filter_value_id']

                # fetch filter value with its filter
                try:
                    filter_value: FilterValue = FilterValue.objects.select_related('filter').get(id=fv_id)
                except FilterValue.DoesNotExist as e:
                    raise FilterValueNotFoundException(cause=e)

                # check allowed for product category
                allowed = CategoryFilter.objects.filter(category=product.category, filter=filter_value.filter).exists()
                if not allowed:
                    raise FilterValueNotAllowedException(cause=None)


                # create assignment (idempotent)
                pfv, _ = ProductFilterValue.objects.get_or_create(product=product, filter_value=filter_value)
                
                created_assignments.append(pfv)


            result_dto = AddFilterValuesForProductResponseDTO(
                assignments=[
                    ProductFilterValueDTO(
                        id=a.id,
                        product_id=a.product.id,
                        filter_value_id=a.filter_value.id,
                        filter_value_name=a.filter_value.name,
                    )
                    for a in created_assignments
                ]
            )

            # After all assignments, generate embedding for the product (best-effort).
            try:
                embedding_text = self._build_embedding_text(product, created_assignments)
                embedding_data = EmbeddingService.generate_embedding(embedding_text)
                # Save embedding if generated
                if embedding_data is not None:
                    product.embedding = embedding_data
                    product.save(update_fields=["embedding"])
            except Exception as e:
                # Don't fail the operation if embedding generation fails; log and continue.
                print(f"Embedding generation failed: {e}")
                
            # Update product active status based on the presence of variants and filter values
            self.__update_product_active_status(product)

            return result_dto

        except Exception as e:
            raise e

    def __update_product_active_status(self, product: Product):
        try:
            product.active = product.variants.exists() and product.filter_values.exists()
            product.save(update_fields=["active"])
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            print(f"Failed to update product active status: {e}")
            raise e

    def __find_product_and_lock(self, product_id: int) -> Product:
        try:
            return Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist as e:
            raise ProductNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _build_embedding_text(self, product: Product, assignments: list[ProductFilterValue]) -> str:
        # Compose a descriptive text using product fields, assigned filter values and variant colors
        parts = []
        parts.append(f"Gender: {product.category.gender}.")
        parts.append(f"Category: {product.category.name}.")
        parts.append(f"Name: {product.name}.")
        parts.append(f"Description: {product.description}.")

        # Filters: group by filter name
        filter_map = {}
        for a in assignments:
            fname = a.filter_value.filter.name
            filter_map.setdefault(fname, []).append(a.filter_value.name)

        for fname, values in filter_map.items():
            values_str = ", ".join(values)
            parts.append(f"{fname}: {values_str}.")

        # Variants (color names)
        variant_colors = [v.color_name for v in product.variants.all()]
        if variant_colors:
            parts.append(f"Variants: {', '.join(variant_colors)}.")

        return " ".join(parts)
