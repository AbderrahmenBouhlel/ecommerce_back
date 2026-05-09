from decimal import Decimal

from django.db import IntegrityError, OperationalError
from django.utils.text import slugify

from classification_app.models import Category
from core.exceptions.excecptions import InternalServerErrorException, ServerUnavailableException
from product_app.apis.create_product.dtos import CreateProductResponseDTO
from product_app.errors import CategoryInactiveException, ProductCategoryNotFoundException, ProductNameAlreadyExistsException
from product_app.models import Product

from core.utils import build_unique_slug


class CreateProductService:
    
    def execute(self, name: str, description: str, price: Decimal, category_id: int) -> CreateProductResponseDTO:
        category_obj = self._find_category(category_id)
        slug = build_unique_slug(name)
        product_obj = self._create_product(
            name=name,
            description=description,
            price=price,
            category=category_obj,
            slug=slug,
        )


        return CreateProductResponseDTO(
            id=product_obj.id,
            status=product_obj.status,
            name=product_obj.name,
            description=product_obj.description,
            price=product_obj.price,
            category_id=product_obj.category_id,
            created_at=product_obj.created_at,
        )

    def _find_category(self, category_id: int) -> Category:
        try:
            category_obj = Category.objects.get(id=category_id)
            if not category_obj.is_active:
                raise CategoryInactiveException()
            return category_obj
        except Category.DoesNotExist as e:
            raise ProductCategoryNotFoundException(cause=e)
        except CategoryInactiveException:
            raise
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)

    def _create_product(self, name: str, description: str, price: Decimal, category: Category, slug: str) -> Product:
        try:
            return Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                slug=slug,
                status="DRAFT",
                embedding=None,
            )
        except IntegrityError as e:
            raise ProductNameAlreadyExistsException(cause=e)
        except OperationalError as e:
            raise ServerUnavailableException(message="Service temporarily unavailable.", cause=e)
        except Exception as e:
            raise InternalServerErrorException(message="Internal server error.", cause=e)
    
