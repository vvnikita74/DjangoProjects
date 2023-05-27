from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('services/', Services.as_view(), name='services'),
    path('club/<slug:club_slug>/', club_page, name='club_page'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete')
]
