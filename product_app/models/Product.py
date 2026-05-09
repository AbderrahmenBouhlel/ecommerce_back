from django.db import models
from classification_app.models import Category

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True , max_length=255)
    
    #a catrgory cant be deleted if it has products , and a product must have a category 
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, blank=False, related_name='products')
    
    
    
    # Stores the array of numbers [0.12, -0.44, ...]
    embedding = models.JSONField(null=True, blank=True)
    
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ARCHIVED', 'Archived'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    
    cover_image_url = models.URLField(null=True, blank=True)
    hover_image_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'product'