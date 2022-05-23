from django.core.validators import MinLengthValidator
from django import forms


class CreateUpdateUserDetails(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=255)
    last_name = forms.CharField(label="Фамилия", max_length=255)
    middle_name = forms.CharField(
        label="Отчество", max_length=255, required=False)
    phone_number = forms.CharField(
        label="Номер телефона", max_length=11, validators=[MinLengthValidator(11)])
    city = forms.CharField(label="Город", max_length=255)
    street = forms.CharField(label="Улица", max_length=255)
    house = forms.CharField(label="Дом", max_length=255)
    housing = forms.CharField(
        label="Подъезд", max_length=255, required=False)
    apartment = forms.CharField(
        label="Квартира", max_length=255, required=False)
    intercom_code = forms.CharField(
        label="Код домофона", max_length=255, required=False)
    card_number = forms.CharField(
        label="Номер банковской карты", max_length=16, validators=[MinLengthValidator(16)])
    expiry_date = forms.CharField(
        label="Срок действия", max_length=5, validators=[MinLengthValidator(5)])
    cvc_code = forms.CharField(
        label="CVC/CVV код", max_length=3, validators=[MinLengthValidator(3)])


class FeedbackForm(forms.Form):
    subject = forms.CharField(label="Тема обращения", max_length=255)
    description = forms.CharField(
        label="Описание обращения", widget=forms.Textarea)
