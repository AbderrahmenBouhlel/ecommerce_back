from itertools import product
from typing import List
from django.db import IntegrityError, OperationalError

from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
    
from product_app.apis.create_product_variant.dtos import CreateProductVariantResponseDTO
from product_app.apis.create_product_variant.dtos.create_product_variant_response import VariantImageDTO
from product_app.apis.create_product_variant.service.add_variant_images_service import AddVariantImagesService
from product_app.errors import ProductNotFoundException
from product_app.models import Product, ProductVariant, ProductVariantImage
from product_app.apis.create_product_variant.exception import DuplicateColorNameInProductException
from django.db import transaction


class CreateProductVariantService:
    
    def __init__(self, addVariantImagesService: AddVariantImagesService):
        self.addVariantImagesService = addVariantImagesService
        
    @transaction.atomic
    def execute(self, product_id: int, color_name: str, color_code: str , images: List[VariantImageDTO]) -> CreateProductVariantResponseDTO:
        product_obj = self._find_product_with_lock(product_id)

        variant_obj: ProductVariant = self._create_variant(
            product=product_obj,
            color_name=color_name,
            color_code=color_code,
        )
        
        created_images: List[ProductVariantImage] = self.addVariantImagesService.excute(
            variant=variant_obj,
            images=images
        )
        
        self._assign_product_preview_images_if_missing(
            product=product_obj,
            created_images=created_images
        )

        return CreateProductVariantResponseDTO(
            id=variant_obj.id,
            product_id=variant_obj.product_id,
            color_name=variant_obj.color_name,
            color_code=variant_obj.color_code,
            created_at=variant_obj.created_at,
            images=created_images
        )
        
        
    def _assign_product_preview_images_if_missing(self,product: Product,created_images: List[ProductVariantImage]) -> None:

        updates = []

        if not product.cover_image_url and len(created_images) >= 1:
            product.cover_image_url = created_images[0].image_url
            updates.append("cover_image_url")

        if not product.hover_image_url and len(created_images) >= 2:
            product.hover_image_url = created_images[1].image_url
            updates.append("hover_image_url")

        if updates:
            product.save(update_fields=updates)

    def _find_product_with_lock(self, product_id: int) -> Product:
        try:
            return Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist as e:
            raise ProductNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _create_variant(self, product: Product, color_name: str, color_code: str) -> ProductVariant:
        try:
            return ProductVariant.objects.create(
                product=product,
                color_name=color_name,
                color_code=color_code,
            )
        except IntegrityError as e:
            raise DuplicateColorNameInProductException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
