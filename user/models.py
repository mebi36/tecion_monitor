from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Company
from django.db.models.deletion import CASCADE
# Create your models here.

class AppUser(AbstractUser):
    company = models.ForeignKey(to=Company, on_delete=CASCADE)
    