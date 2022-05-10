from django.db import models
from django.urls import reverse

from item.models import Item
from company.models import Company
from django.db.models.deletion import CASCADE

# Create your models here.
class Monitor(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(to=Item, on_delete=CASCADE)
    company = models.ForeignKey(to=Company, on_delete=CASCADE)
    oil_level = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    ignition = models.BooleanField(null=True)
    fuel_level = models.DecimalField(max_digits=5, decimal_places=2)
    time_stamp = models.DateTimeField()
    doors = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["time_stamp", "item", "company"],
                name="unique_item_value",
            )
        ]
