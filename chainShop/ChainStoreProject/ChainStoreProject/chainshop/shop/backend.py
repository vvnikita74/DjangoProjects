from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        user = CustomUser.objects.get(email=email)
        if user and user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None