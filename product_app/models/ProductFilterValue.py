from django.db import models
from django.forms import ValidationError
from classification_app.models import FilterValue
from product_app.models import Product
from classification_app.models import CategoryFilter

from classification_app.errors import FilterValueNotAllowedError



class ProductFilterValue(models.Model):
  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='filter_values' , db_column='product_id')
    filter_value = models.ForeignKey(FilterValue, on_delete=models.CASCADE, related_name='products' , db_column='filter_value_id')

    def __str__(self):
        return f"{self.product}: {self.filter_value}"
    
    
    
    def assert_valide_filter_value(self):
        productCategory = self.product.category
        
        # the filter that the filter value belongs to
        filter_id = self.filter_value.filter.id
        
        category_allowed_filters = CategoryFilter.objects.filter(category=productCategory).values_list('filter_id', flat=True)
        if (filter_id not in category_allowed_filters):
            raise FilterValueNotAllowedError(f"The filter value '{self.filter_value.name}' is not allowed for the category '{productCategory.name}' of the product '{self.product.name}'.")
        
        
    
    def save(self, *args, **kwargs):
        self.assert_valide_filter_value()  
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'product_filter_value'
        constraints = [
            models.UniqueConstraint(fields=['product', 'filter_value'], name='unique_product_filter_value')
        ]