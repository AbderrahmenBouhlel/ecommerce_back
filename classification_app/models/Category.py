from django.db import models
from .Filter import Filter


class Category(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    gender = models.CharField(max_length=10, choices=Gender.choices)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
  
    class Meta:
        db_table = "categories"
        constraints = [
            models.UniqueConstraint(fields=["name", "gender"], name="unique_category_name_gender"),
        ]

    def __str__(self):
        return self.name