from django.db import models
from django.db.models.deletion import PROTECT
from django.urls.base import reverse

from company.models import Company


class ItemType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)


# Create your models here.
class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.ForeignKey(to=ItemType, on_delete=PROTECT)
    description = models.CharField(
        "Owner's description given about the item", max_length=255, null=True
    )
    company = models.ForeignKey(to=Company, on_delete=PROTECT)

    # def __str__(self):
    #     return f"{self.type.name} - {self.id}"

    def get_dashboard_url(self):
        return reverse("monitor:dashboard", kwargs={"item_id": self.id})

    def get_latest_data_url(self):
        return reverse("monitor:latest_data", kwargs={"item_id": self.id})
