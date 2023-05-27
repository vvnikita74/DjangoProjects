from django import forms
from django.http import request
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class OrderForm (forms.ModelForm):
    def __init__(self, *args, **kwargs):
        center_id = kwargs.pop('center_id', None)
        super().__init__(*args, **kwargs)
        if center_id:
            self.fields['center_title'].empty_label = "Центр не выбран"
            self.fields['worker'].empty_label = "Тренер не выбран"
            self.fields['activity'].empty_label = "Занятие не выбрано"
            self.fields['center_title'].queryset = FitnessCenter.objects.filter(id=center_id)
            self.fields['worker'].queryset = Employer.objects.filter(work_center=center_id)
            actL = list(Employer.objects.filter(work_center=center_id).values('activity_id'))
            self.fields['activity'].queryset = Employer.objects.filter(work_center=center_id)
            activities_list = []
            for act in actL:
                activities_list.append(act['activity_id'])
            self.fields['activity'].queryset = Activities.objects.filter(id__in=activities_list)

    class Meta:
        model = OrderList
        fields = ['center_title', 'worker', 'activity', 'date']


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", max_length=50)
    full_name = forms.CharField(label="ФИО", max_length=100)
    email = forms.EmailField(label="Электронная почта")
    phone_number = forms.CharField(label="Номер телефона", max_length=12)
    password1 = forms.CharField(label=" Пароль")
    password2 = forms.CharField(label="Повторите пароль")

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'phone_number', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
