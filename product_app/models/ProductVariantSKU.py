from django.db import models

from product_app.models import ProductVariant





class ProductVariantSKU(models.Model):
    
    
    size = models.CharField(max_length=255)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='skus' , db_column='product_variant_id')
    
    stock = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)
    
    sku = models.CharField(max_length=255, unique=True)
  

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'product_variant_sku'
        constraints = [
            models.UniqueConstraint(fields=['size', 'product_variant'], name='unique_size_product_variant')
        ]

    def __str__(self):
        return self.size