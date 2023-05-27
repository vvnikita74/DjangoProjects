from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

phone_valid = [
    MinValueValidator(10000000000), MaxValueValidator(100000000000)
]


class CustomUser(AbstractUser):
    phone_number = models.PositiveIntegerField(verbose_name='Номер телефона', unique=True, validators=phone_valid)
    profile_image = models.ImageField(upload_to="PCClub/images/%Y/user_avatar/%m/", verbose_name="Фото профиля", default="avatar_default.png", null=True, blank=True)
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id']


class Tariff(models.Model):
    device_choice = [('P', 'Компьютер'), ('C', 'Консоль')]
    title = models.CharField(verbose_name="Название", max_length=100, unique=True, blank=False, null=False)
    device = models.CharField(verbose_name="Тип устройства", choices=device_choice, default = "P", max_length=2)
    characteristics = models.TextField(verbose_name="Характеристики ПК", null=False, blank=False)
    periphery = models.TextField(verbose_name="Периферия", null=False, blank=False)
    photo = models.ImageField(upload_to='PCClub/images/tariff_photo/', verbose_name='Фото', default="default_tariff_photo.png", null=True, blank=True)
    cost = models.PositiveIntegerField(verbose_name="Стоимость за час", validators=[MinValueValidator(50)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ['id', 'cost']


class Clubs(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100, unique=True, blank=False, null=False)
    slug = models.SlugField(verbose_name="Url", max_length=255, unique=True, db_index=True)
    email = models.EmailField(verbose_name="Электронная почта", max_length=100)
    manager_phone = models.PositiveIntegerField(verbose_name='Телефон', validators=phone_valid)
    location = models.CharField(verbose_name="Адрес", max_length=100, unique=True, blank=False, null=False)
    tariffs = models.ManyToManyField(Tariff)
    photo = models.ImageField(upload_to='PCClub/images/club_photo/', verbose_name='Фото', default="default_tariff_photo.png", null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('club_page', kwargs={'club_slug': self.slug})

    class Meta:
        verbose_name = "Компьютерный клуб"
        verbose_name_plural = "Компьютерные клубы"
        ordering = ['id', 'title']


class Orders(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, verbose_name="Пользователь")
    club = models.ForeignKey("Clubs", on_delete=models.CASCADE, verbose_name="Клуб")
    tariff = models.ForeignKey("Tariff", on_delete=models.CASCADE, verbose_name="Тариф")
    hours = models.IntegerField(verbose_name="Время")
    cost = models.PositiveIntegerField(verbose_name="Стоимость")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "заказа"
        verbose_name_plural = "Заказы"
        ordering = ['date']

