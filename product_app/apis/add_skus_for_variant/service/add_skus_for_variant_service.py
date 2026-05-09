import uuid
from typing import List

from django.db import transaction, IntegrityError, OperationalError

from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from product_app.apis.add_skus_for_variant.dtos import AddSkusForVariantResponseDTO, SkuDTO
from product_app.apis.add_skus_for_variant.dtos.add_skus_request import AddSkusForVariantRequestDTO
from product_app.models import ProductVariant, ProductVariantSKU, Product
from product_app.apis.add_skus_for_variant.exception.exception import ProductArchivedException, DuplicateSizeInVariantException
from product_app.errors import ProductVariantNotFoundException


class AddSkusForVariantService:
    @transaction.atomic
    def execute(self, request_dto: AddSkusForVariantRequestDTO) -> AddSkusForVariantResponseDTO:
        created_skus: List[ProductVariantSKU] = []

        try:
            variant: ProductVariant = self.__find_variant_and_lock(request_dto.variant_id)

            # check product status
            if variant.product.status == 'ARCHIVED':
                raise ProductArchivedException()

            for sku_item in request_dto.skus:
                size = sku_item['size']
                stock = sku_item['stock']

                sku_obj = self.__create_sku(variant, size, stock)
                created_skus.append(sku_obj)

            result_dto = AddSkusForVariantResponseDTO(
                skus=[
                    SkuDTO(
                        id=s.id,
                        size=s.size,
                        stock=s.stock,
                        reserved=s.reserved,
                        sku_code=s.sku,
                    )
                    for s in created_skus
                ]
            )

            return result_dto

        except Exception as e:
            raise e

    def __find_variant_and_lock(self, variant_id: int) -> ProductVariant:
        try:
            return ProductVariant.objects.select_related('product').select_for_update().get(id=variant_id)
        except ProductVariant.DoesNotExist as e:
            raise ProductVariantNotFoundException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def __create_sku(self, variant: ProductVariant, size: str, stock: int) -> ProductVariantSKU:
        try:
            sku_code = self.__generate_sku_code(variant, size)
            return ProductVariantSKU.objects.create(
                product_variant=variant,
                size=size,
                stock=stock,
                sku=sku_code,
            )
        except IntegrityError as e:
            # Detect duplicate size in variant
            raise DuplicateSizeInVariantException(cause=e, message=f"A SKU with the same size {size} already exists for this variant.")
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def __generate_sku_code(self, variant: ProductVariant, size: str) -> str:
        # Generate a server-side SKU code. Simple pattern: <PRODUCT_ID>-<VARIANT_ID>-<COLOR_NAME>-<SIZE>-<SHORTUUID>
        short = uuid.uuid4().hex[:8].upper()
        return f"P{variant.product.slug}-V{variant.id}-{variant.color_name}-{size}-{short}"
