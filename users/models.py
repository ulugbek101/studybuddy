from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(upload_to='users/', null=True, default='users/avatar.svg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    @property
    def get_name(self):
        return self.name if self.name else ''
