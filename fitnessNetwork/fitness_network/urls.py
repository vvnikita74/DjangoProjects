from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('centers/<int:center_id>/', center_page, name="center_page"),
    path('activity/<int:center_id>/', activity_page, name="activity_page"),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_page, name='profile')
]

