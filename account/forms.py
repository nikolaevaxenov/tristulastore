from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateUpdateUserDetails(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=255)
    last_name = forms.CharField(label="Фамилия", max_length=255)
    middle_name = forms.CharField(
        label="Отчество", max_length=255, required=False)
    phone_number = forms.IntegerField(label="Номер телефона", validators=[
        MinValueValidator(70000000000),
        MaxValueValidator(79999999999)
    ])


class CreateUpdateUserAddress(forms.Form):
    city = forms.CharField(label="Город", max_length=255)
    street = forms.CharField(label="Улица", max_length=255)
    house = forms.CharField(label="Дом", max_length=255)
    housing = forms.CharField(
        label="Подъезд", max_length=255, required=False)
    apartment = forms.CharField(
        label="Квартира", max_length=255, required=False)
    intercom_code = forms.CharField(
        label="Код домофона", max_length=255, required=False)


class CreateUpdateUserCard(forms.Form):
    card_number = forms.CharField(
        label="Номер банковской карты", max_length=16, validators=[MinLengthValidator(16)])
    expiry_date = forms.CharField(
        label="Срок действия", max_length=5, validators=[MinLengthValidator(5)])
    cvc_code = forms.CharField(
        label="CVC/CVV код", max_length=3, validators=[MinLengthValidator(3)])
