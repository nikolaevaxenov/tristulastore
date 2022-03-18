from django.contrib.postgres.fields import ArrayField
from django.db import models
import string
import random


def productPath(instance, filename):
    return f"store/static/store/products_photo/product_{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}.{filename.split('.')[-1]}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    description = models.TextField()
    colors = ArrayField(models.CharField(
        max_length=200), blank=False, null=True)
    photo = models.ImageField(upload_to=productPath)
    price = models.IntegerField()
    sale_price = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Products"
