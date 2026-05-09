from django.db import models

from product_app.models import Product





class ProductVariant(models.Model):
    color_code = models.CharField(max_length=255, null=False, blank=False)
    color_name = models.CharField(max_length=255 ,null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
  


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'product_variant'
        constraints = [
            models.UniqueConstraint(fields=['color_name', 'product'], name='unique_color_name_per_product')
        ]

    def __str__(self):
        return self.color_name