from django.db import models


class Filter(models.Model):
    name = models.CharField(max_length=150 , unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = "filters"
        ordering = ["id"]  

    def __str__(self):
        return self.name