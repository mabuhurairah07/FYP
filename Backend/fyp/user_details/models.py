from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.
class UserDetails(AbstractUser):
    id = models.AutoField(primary_key=True)
    address = models.TextField(max_length=2000, default='')
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phoneRegex = RegexValidator(regex=r"^\+?\d{8,15}$")
    phone_no = models.CharField(validators=[phoneRegex], max_length = 16, unique=True, null = False, default='')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)