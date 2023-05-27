from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import *
from django.core.validators import MinValueValidator


phone_valid = [MinPhoneValid(10000000000), MaxPhoneValid(100000000000)]


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone_number, password=None):

        if not email:
            raise ValueError('Необходимо заполнить поле адреса электронной почты')
        if not phone_number:
            raise ValueError('Необходимо заполнить поле номера телефона')

        user = self.model(email=self.normalize_email(email), phone_number=phone_number,)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone_number, password=None):
        user = self.create_user(email, phone_number, password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True, blank=False, null=False)
    name = models.CharField(verbose_name='ФИО', max_length=100, null=True)
    phone_number = models.PositiveIntegerField(verbose_name="Номер телефона", validators=phone_valid, null=True)
    image = models.ImageField(upload_to='hospapp/image/user_image/', verbose_name='Фото', null=True, blank=True)
    is_doctor = models.BooleanField(default=False, verbose_name='Права доктора')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return str(self.name)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id']


class Services(models.Model):
    title = models.CharField(verbose_name="Название услуги", max_length=100, null=False, blank=False)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    cost = models.PositiveIntegerField(verbose_name="Стоимость", validators=[MinValueValidator(500)])
    photo = models.ImageField(upload_to='hospapp/image/service_photo/', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['id']


class Doctors(models.Model):
    user = models.ForeignKey('CustomUser', verbose_name='Пользователь доктора', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hospapp/image/doctors_photo/', verbose_name='Фото', null=True, blank=True)
    services = models.ManyToManyField('Services', verbose_name='Услуги')

    def __str__(self):
        return str(self.user.name)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['id']


class Receptions(models.Model):
    client = models.ForeignKey('CustomUser', verbose_name='Клиент', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctors', verbose_name='Доктор', on_delete=models.CASCADE)
    service = models.ForeignKey('Services', verbose_name='Услуга', on_delete=models.CASCADE)
    is_close = models.BooleanField(verbose_name='Закрыт', default=False)
    date = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return f"{self.client} - {self.doctor} - {self.date}"

    class Meta:
        verbose_name = 'Прием'
        verbose_name_plural = 'Приемы'
        ordering = ['date']


