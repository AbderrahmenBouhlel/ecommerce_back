from datetime import datetime

from traitlets import List

from core.apiResponse.response import BaseDTO
from product_app.models import ProductVariantImage


class VariantImageDTO(BaseDTO):
	def __init__(self, id: int, image_url: str, order: int):
		self.id = id
		self.image_url = image_url
		self.order = order

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"image_url": self.image_url,
			"order": self.order,
		}


class CreateProductVariantResponseDTO(BaseDTO):
    def __init__(self, id: int, product_id: int, color_name: str, color_code: str, created_at: datetime , images: List[ProductVariantImage]):
        self.id = id
        self.product_id = product_id
        self.color_name = color_name
        self.color_code = color_code
        self.created_at = created_at
        self.images = [
            VariantImageDTO(
                id=image.id,
                image_url=image.image_url,
                order=image.order
            ) for image in images
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "color_name": self.color_name,
            "color_code": self.color_code,
            "created_at": self.created_at.isoformat(),
            "images": [image.to_dict() for image in self.images],
        }
