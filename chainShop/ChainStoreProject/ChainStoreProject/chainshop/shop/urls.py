from django.urls import path
from .views import *

urlpatterns = [
    
    path('', index, name='index'),
    path('category/<slug:category_slug>', cat_products, name='products_by_category'),
    path('about/', about, name='about'),
    path('product/<slug:slug>', product, name='product'),
    
    path('auth/login', login_view, name='login'),
    path('auth/register', Register.as_view(), name='register'),
    path('auth/logout', logout_user, name='logout'),
    path('profile', profile, name='profile'),


    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
]