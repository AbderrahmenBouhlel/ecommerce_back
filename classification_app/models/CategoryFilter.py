from django.db import models
from .Category import Category
from .Filter import Filter



class CategoryFilter(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        db_column='category_id',
        related_name='category_filters'
    )
    filter = models.ForeignKey(
        Filter, 
        on_delete=models.CASCADE , 
        db_column='filter_id',
        related_name='filter_categories'
    )
    
    
    class Meta:
        db_table = "category_filters"
        constraints = [
            models.UniqueConstraint(
                fields=["category", "filter"],
                name="unique_category_filter"
            )
        ]