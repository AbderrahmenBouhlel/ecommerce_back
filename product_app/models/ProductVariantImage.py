


from django.db import models

from product_app.models import ProductVariant



class ProductVariantImage(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=512)
    
    order = models.PositiveIntegerField(blank=False,null=False) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'product_variant_image'
        constraints = [
            models.UniqueConstraint(fields=['product_variant', 'image_url'], name='unique_image_url_per_variant'),
            models.UniqueConstraint(fields=['product_variant', 'order'], name='unique_image_order_per_variant'),
        ]
        ordering = ['order'] # Default database-level sorting

    def __str__(self):
        return self.image_url