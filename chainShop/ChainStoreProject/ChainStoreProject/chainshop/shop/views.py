from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from cart.context_processor import cart_total_amount


#--------------Товары-----------------
def index (request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'cats':categories, 'products': products})


def cat_products(request, category_slug):
    products = Product.objects.filter(category__slug = category_slug)
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {'cats':categories, 'products': products})


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    return render(request, "shop/product.html", {"product": product, "cats":categories})


#----------Авторизация-------------

def login_view(request):
    categories = Category.objects.all()
    if request.method == "POST":

        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "shop/login.html", {'errors': 'Неправильные данные'})

    return render(request, "shop/login.html", {'cats':categories})


class Register(CreateView):

    form_class = UserCreationForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        return redirect('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        return context
    
    
def logout_user(request):
    logout(request)
    return redirect('index')


#--------Прочее----------------
def profile(request):
    categories = Category.objects.all()
    return render(request, 'shop/profile.html', {'cats':categories})


def about(request):
    categories = Category.objects.all()
    return render(request, 'shop/about.html', {'cats':categories})

#--------------Корзина-------------
@login_required(login_url=reverse_lazy('login'))
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_detail(request):
    total = cart_total_amount(request)['cart_total_amount']
    if total:
        return render(request, 'shop/cart.html', {'total': total, 'cats': Category.objects.all()})
    else:
        return redirect("index")