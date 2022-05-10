from django.db import models

# from django.db.models.deletion import CASCADE, PROTECT

# Create your models here.
class Sector(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    # sector = models.ManyToManyField(to=Sector)
