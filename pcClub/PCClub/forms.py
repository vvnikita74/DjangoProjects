from django import forms
from django.http import request
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(label="Номер телефона", max_length=12)
    profile_image = forms.ImageField(label='Фото профиля')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'profile_image', 'password1', 'password2')

    def clean_email(self):
        user_mail = self.cleaned_data['email']
        if CustomUser.objects.filter(email=user_mail).exists():
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')
        return user_mail


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', None)
        super().__init__(*args, **kwargs)
        if club:
            self.fields['tariff'].empty_label = "Выбрать тариф"
            self.fields['tariff'].queryset = Clubs.objects.filter(title=club)[0].tariffs.all()

    def clean_hours(self):
        hours = self.cleaned_data['hours']
        if hours > 24 or hours <= 0:
            raise ValidationError()
        return hours

    class Meta:
        model = Orders
        fields = ['tariff', 'hours']
