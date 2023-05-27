from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email=None, phone_number=None, password=None):

        if not email:
            raise ValueError('Поле электронной почты является обязательным')
        if not phone_number:
            raise ValueError('Поле номера телефона является обязательным')

        user = self.model(email=self.normalize_email(email), phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone_number, password=None):

        user = self.create_user(email, phone_number, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user