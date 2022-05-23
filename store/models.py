from itertools import product
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from datetime import date
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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Orders"


class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    class Meta:
        verbose_name_plural = "Order Products"


class Feedback(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField()
    checked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Feedbacks"


class Event(models.Model):
    event = models.CharField(max_length=255)
    date = models.DateField(default=date.today)

    class Meta:
        verbose_name_plural = "Events"
