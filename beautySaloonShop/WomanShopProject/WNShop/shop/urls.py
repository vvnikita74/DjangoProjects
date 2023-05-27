from django.urls import path
from .views import *

urlpatterns = [

    path('', index, name='home'),
    
    path('auth/login', login_view, name='login'),
    path('auth/register', Register.as_view(), name='register'),
    path('auth/logout', logout_user, name='logout'),
    
    path('profile', profile, name='profile'),
    path('about', about_page, name='about'),
    path('order', make_order, name='make_order'),
    
    path('products', products_page, name='products'),
    path('products/<slug:category_slug>', products_page, name='products_by_category'),
    path('product/<slug:slug>', product, name='product'),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
    
    path('file/<str:filename>/', download_file, name='download_file')
]