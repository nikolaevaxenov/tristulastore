from django.db import models
from django.contrib.auth.models import User


class User_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "User Details"


class User_Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    housing = models.CharField(max_length=255, blank=True, null=True)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    intercom_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Addresses"


class User_Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=255)
    cvc_code = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "User Cards"
