from core.apiResponse.response import BaseDTO


class CategoryCatalogProductDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        price: object,
        cover_image_url: str | None,
        hover_image_url: str | None,
        is_active: bool,
        filter_values: list["CategoryCatalogFilterValueDTO"] | None = None,
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.price = price
        self.cover_image_url = cover_image_url
        self.hover_image_url = hover_image_url
        self.is_active = is_active
        self.filter_values = filter_values or []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "price": float(self.price),
            "cover_image_url": self.cover_image_url,
            "hover_image_url": self.hover_image_url,
            "is_active": self.is_active,
            "filter_values": [fv.to_dict() for fv in self.filter_values],
        }


class CategoryCatalogFilterValueDTO(BaseDTO):
    def __init__(self, id: int, name: str, slug: str):
        self.id = id
        self.name = name
        self.slug = slug

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
        }


class GetCategoryCatalogResponseDTO(BaseDTO):
    def __init__(
        self,
        products: list[CategoryCatalogProductDTO],
        filter_values: list[CategoryCatalogFilterValueDTO],
    ):
        self.products = products
        self.filter_values = filter_values

    def to_dict(self) -> dict:
        return {
            "products": [product.to_dict() for product in self.products],
            "filter_values": [filter_value.to_dict() for filter_value in self.filter_values],
        }
