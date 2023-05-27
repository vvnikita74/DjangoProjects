from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class FitnessCenter (models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    contract_number = models.PositiveIntegerField(unique = True, verbose_name="Договор №")
    city = models.CharField(max_length=40, verbose_name="Идентификатор города")
    location = models.CharField(max_length=100, verbose_name="Адрес")
    manager_phone = models.CharField(max_length=15, verbose_name="Номер телефона для связи")
    email = models.EmailField(max_length=50, verbose_name="Электронная почта для связи")
    photo = models.ImageField(upload_to="fitness_network/images/%Y/%m/", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('center_page', kwargs={'center_id': self.id})

    class Meta:
        verbose_name = "фитнес-центр"
        verbose_name_plural = "Фитнес-центры"
        ordering = ['id']


class Activities (models.Model):
    title = models.CharField(max_length=50, verbose_name="Наименование")
    cost = models.PositiveIntegerField(verbose_name="Стоимость")
    description = models.TextField(blank=True, verbose_name="Описание")
    article = models.CharField(max_length=50, verbose_name="Артикул")
    photo = models.ImageField(upload_to="fitness_network/images/%Y/%m/", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "занятие"
        verbose_name_plural = "Занятия"
        ordering = ['id']


class Employer (models.Model):
    name = models.CharField(max_length=50, verbose_name="ФИО")
    activity = models.ForeignKey('Activities', on_delete=models.PROTECT, verbose_name="Вид работы")
    work_center = models.ForeignKey('FitnessCenter', on_delete=models.PROTECT, verbose_name="Место работы")
    salary = models.PositiveIntegerField(verbose_name="Зарплата")
    photo = models.ImageField(upload_to="fitness_network/images/%Y/%m/", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "сотрудника"
        verbose_name_plural = "Сотрудники"
        ordering = ['id']


class OrderList (models.Model):
    center_title = models.ForeignKey('FitnessCenter', on_delete=models.PROTECT, verbose_name="Фитнес-центр", max_length=100)
    user = models.ForeignKey('CustomUser', verbose_name='Пользователь', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activities',verbose_name="Занятие", on_delete=models.PROTECT)
    worker = models.ForeignKey('Employer', verbose_name="Тренер", on_delete=models.PROTECT)
    date = models.DateTimeField(null=True, verbose_name='Дата')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "заказа"
        verbose_name_plural = "Заказы"
        ordering = ['order_date']


class CustomUser(AbstractUser):
    full_name = models.CharField('ФИО', max_length=100, default='')
    phone_number = models.CharField('Номер телефона', max_length=11, default='')