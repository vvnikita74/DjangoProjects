from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import user_required, doc_required
from .models import *
from .forms import UserCreationForm, AddRecept


def index(request):
    title = "Поликлиника - Главная страница"
    service = Services.objects.all()
    return render(request, 'hospapp/index.html', {'title': title, 'services': service})


class Register(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'hospapp/register.html'
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Поликлиника - Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'hospapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Поликлиника - Авторизация"
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url=reverse_lazy('login'))
@user_required(login_url=reverse_lazy('home'))
def profile(request):
    title = "Поликлиника - Профиль"
    if request.user.is_admin:
        return render(request, 'hospapp/profile_admin.html', {'title': title})
    else:
        try:
            recepts = Receptions.objects.filter(client=request.user, is_close=False)
        except:
            recepts = []
        return render(request, 'hospapp/profile.html', {'title': title, 'recepts': recepts})


@login_required(login_url=reverse_lazy('login'))
@user_required(login_url=reverse_lazy('home'))
def appointment(request):
    title = "Поликлиника - Запись к специалистам"
    doctors = Doctors.objects.all()
    return render(request, 'hospapp/to_doc.html', {'title': title, 'doctors': doctors})


@login_required(login_url=reverse_lazy('login'))
@user_required(login_url=reverse_lazy('home'))
def recept(request, doc_id):
    title = "Поликлиника - Запись"
    doctor = Doctors.objects.filter(id=doc_id)[0]

    if request.method == 'POST':
        form = AddRecept(request.POST)
        form.instance.client = request.user
        form.instance.doctor = Doctors.objects.filter(id=doc_id)[0]
        form.save(commit=False)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddRecept(doc=doc_id)

    doctor = Doctors.objects.filter(id=doc_id)[0]
    return render(request, 'hospapp/recept.html', {'title': title, 'doctor': doctor, 'form': form})


@login_required(login_url=reverse_lazy('login'))
@doc_required(login_url=reverse_lazy('home'))
def doc_page(request):
    title = f"Приемы - {request.user.name}"
    doc = Doctors.objects.filter(user=request.user)[0]
    receptions = Receptions.objects.filter(doctor=doc)

    return render(request, 'hospapp/doc_page.html', {'title': title, 'receptions': receptions})


@login_required(login_url=reverse_lazy('login'))
@doc_required(login_url=reverse_lazy('home'))
def close_receptions(request, rec_id):

    reception = Receptions.objects.filter(id=rec_id)[0]
    reception.is_close = True
    reception.save()
    return redirect('doc_page')