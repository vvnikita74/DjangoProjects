from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cart.cart import Cart
from cart.context_processor import cart_total_amount
import mimetypes
from .make_PDF import create_pdf
from datetime import datetime


def index(request):
    return render(request, "shop/index.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, email=username, phone_number=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "shop/login.html", {'errors': 'Неправильные данные'})

    return render(request, "shop/login.html")


class Register(CreateView):

    form_class = UserCreationForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        
        return redirect('home')


def products_page(request, category_slug=None):

    if not category_slug:
        products = Product.objects.all()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop/products.html', {'cats': Category.objects.all(), 'is_all': True, 'products': products, 'page_obj': page_obj})
    
    else:
        active_cat = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category__slug = category_slug)
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop/products.html', {'cats': Category.objects.all(), 'active_cat': active_cat, 'products': products, 'page_obj': page_obj})
    

def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    user_files_names = Orders.objects.filter(user=request.user)
    file_names = {}
    for file in user_files_names:
        file_names[file.date] = file.file
    return render(request, 'shop/profile.html', {'files': file_names})


def about_page(request):
    return render(request, 'shop/about.html')


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product.html', {'product': product})


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
        return render(request, 'shop/cart.html', {'total': total})
    else:
        return redirect("products")


@login_required(login_url=reverse_lazy('login'))
def make_order(request):
    
    cart = Cart(request)
    order_products = []
    total_cost = 0
    user = None
    for key, value in cart.cart.items():
        if user is None:
            user = value['userid']
        order_products.append(value['name'])
        total_cost = total_cost + int(value['quantity'])*float(value['price'])

    user = CustomUser.objects.filter(id=user).first()
    
    current_time = datetime.now()
    date_time = current_time.strftime("%Y-%m-%d_%H-%M")

    create_pdf(str(user), order_products, date_time, total_cost)
    file_name = f"{str(user)}_order_{date_time}.pdf"

    order = Orders()
    order.user = user
    order.date = date_time
    order.file = file_name
    order.save()

    cart.clear()
    return redirect('profile')


def download_file(request, filename):
    fl_path = f"orders/{filename}"
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
