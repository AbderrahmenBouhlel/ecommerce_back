from typing import List
from core.apiResponse.response import BaseDTO


class SkuDTO(BaseDTO):
    def __init__(self, id: int, size: str, stock: int, reserved: int, sku_code: str):
        self.id = id
        self.size = size
        self.stock = stock
        self.reserved = reserved
        self.sku_code = sku_code

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "size": self.size,
            "stock": self.stock,
            "reserved": self.reserved,
            "sku_code": self.sku_code,
        }


class AddSkusForVariantResponseDTO(BaseDTO):
    def __init__(self, skus: List[SkuDTO]):
        self.skus = skus

    def to_dict(self) -> list[dict]:
        return [s.to_dict() for s in self.skus]
