from datetime import datetime
from decimal import Decimal

from core.apiResponse.response import BaseDTO


class CreateProductResponseDTO(BaseDTO):
    def __init__(
        self,
        id: int,
        status: str,
        name: str,
        description: str,
        price: Decimal,
        category_id: int,
        created_at: datetime,
    ):
        self.id = id
        self.status = status
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "categoryId": self.category_id,
            "createdAt": self.created_at.isoformat(),
        }