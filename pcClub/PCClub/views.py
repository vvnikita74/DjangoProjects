from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetDoneView
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import CreateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.db.models import Sum


def index(request):
    First_Club = Clubs.objects.get(pk=1)
    AllClub = Clubs.objects.filter(pk__gte=2)
    return render(request, 'pcclub/index.html', {'fclub': First_Club, 'clubs': AllClub})


class Services(ListView):
    model = Tariff
    template_name = 'pcclub/services.html'
    context_object_name = 'service'


def club_page(request, club_slug):
    club = Clubs.objects.filter(slug=club_slug)[0]

    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            form.instance.user = request.user
            form.instance.club = club
            form.save(commit=False)
            price = int(Tariff.objects.filter(title=form.cleaned_data['tariff']).values('cost')[0].get('cost'))
            form.instance.cost = form.cleaned_data['hours'] * price
            if form.is_valid():
                form.save()
                form = OrderForm(club=club)
        except:
            form.add_error('hours', 'Введите корректное время')
    else:
        form = OrderForm(club=club)

    return render(request, 'pcclub/club_page.html', {'club': club, 'form': form})


def profile(request):
    if request.user.id is not None and not request.user.is_superuser:
        user = CustomUser.objects.filter(id=request.user.id)[0]
        orders = Orders.objects.filter(user=request.user)
        return render(request, 'pcclub/profile.html', {'user': user, 'orders': orders})
    elif request.user.is_superuser:
        clubs_orders = []
        for C in Clubs.objects.values('id', 'title'):
            clubs_orders.append(
                [
                    {'Клуб': C.get('title')},
                    {'Количество заказов': Orders.objects.filter(club=C.get('id')).count()},
                    {'Общая прибыль': Orders.objects.filter(club=C.get('id')).aggregate(Sum('cost')).get('cost__sum')}
                ]
            )
        orders = Orders.objects.all()
        return render(request, 'pcclub/profile_admin.html', {'clubs_orders': clubs_orders, 'orders': orders})
    else:
        return render(request, 'pcclub/register.html')


class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'pcclub/register.html'
    success_url = reverse_lazy("home")


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'pcclub/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('home')


class PasswordReset(PasswordResetView):
    template_name = 'pcclub/pass_res.html'
    email_template_name = 'pcclub/pass_res_mail.html'

    def get_success_url(self):
        return reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'pcclub/pass_res_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'pcclub/pass_res_confirm.html'

    def get_success_url(self):
        return reverse_lazy('password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'pcclub/pass_res_complete.html'
