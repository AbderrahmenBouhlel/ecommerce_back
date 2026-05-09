from django.db import models
from .Filter import Filter



class FilterValue(models.Model):
    filter = models.ForeignKey(
        Filter,
        on_delete=models.CASCADE,
        related_name="values",
        db_column="filter_id"
    )

    name = models.CharField(max_length=150 , unique=True , blank=False)
    description = models.TextField(null=False , default="")
    slug = models.SlugField(null=False, unique=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "filter_values"
        indexes = [
            models.Index(fields=["filter_id"]),
            models.Index(fields=["slug"]),
        ]
        ordering = ["id"]   

    def __str__(self):
        return f"{self.filter.name} - {self.name}"