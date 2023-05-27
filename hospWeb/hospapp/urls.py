from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('doctors/', appointment, name='doc_app'),
    path('recept/<int:doc_id>', recept, name='recept'),
    path('docreceptions/', doc_page, name='doc_page'),
    path('closerecept/<int:rec_id>', close_receptions, name='close_reception'),
]