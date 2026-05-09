from django.db import models




class User(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash  = models.BinaryField(max_length=60 , default=b'')  # bcrypt hash is 60 bytes
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'users'