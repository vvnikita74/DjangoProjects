from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password', 'is_doctor', 'is_admin')


class AddRecept(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        doc = kwargs.pop('doc', None)
        super().__init__(*args, **kwargs)
        if doc:
            self.fields['service'].empty_label = "Выбрать услугу"
            self.fields['service'].queryset = Doctors.objects.filter(id=doc)[0].services.all()

    class Meta:
        model = Receptions
        fields = ('service', 'date')


