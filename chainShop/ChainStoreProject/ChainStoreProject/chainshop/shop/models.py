from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    
    email = models.EmailField("Адрес электронной почты", unique=True, blank=False)
    is_admin = models.BooleanField("Администратор", default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'


    @property
    def is_staff(self):
        return self.is_admin
    
    def __str__(self):
        return(self.email)
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
   

    class Meta:
        
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['id', 'email']



class Category(models.Model):

    name = models.CharField('Название категории', max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True)


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])


    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"
        ordering = ['-name', '-id']


class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField("Название продукта", max_length=150, db_index=True)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    image = models.ImageField("Изображение",upload_to='product/', blank=True)
    description = models.TextField("Описание",max_length=1000, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    available = models.BooleanField("Доступность",default=True)
    created = models.DateTimeField("Создано", auto_now_add=True)
    uploaded = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return  self.name

    def get_absolute_url(self):
        return reverse('product', args=[self.id, self.slug])