from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import *
from django.views.generic import CreateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


def index(request):
    centers = FitnessCenter.objects.all()
    center_act_dict = {}
    for center in FitnessCenter.objects.values('id', 'title'):
        cen_id = center['id']
        center_act_dict[center['title']] = Employer.objects.filter(work_center=cen_id).count()
    if request.user.id is not None:
        user = CustomUser.objects.filter(id=request.user.id)[0]
    else:
        user = None
    return render(request, 'index.html',
                  {'centers': centers, 'user': user, 'centers_act_count': center_act_dict})


def center_page(request, center_id):
    center_info = FitnessCenter.objects.filter(id=center_id)[0]
    employers = Employer.objects.filter(work_center_id=center_id)
    employers_count = len(employers)
    activities = Activities.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Ошибка добавление заказа, попробуйте еще раз')
    else:
        form = OrderForm(center_id=center_id)
    return render(request, 'center.html',
                  {'center': center_info, 'employers': employers, 
                   'wcount': employers_count, 'activities': activities, 
                   'form': form})


def activity_page(request, center_id):
    center_info = FitnessCenter.objects.filter(id=center_id)[0]
    acts_id = Employer.objects.filter(work_center_id=center_id).values('activity_id')
    acts_id_list = []
    for act_id in acts_id:
        acts_id_list.append(act_id['activity_id'])
    activities = Activities.objects.filter(id__in=acts_id_list)
    return render(request, 'activity.html', {'center': center_info, 'acts_info': activities})


class Register(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def profile_page(request):
    if request.user.id is not None and request.user.is_superuser:
        user_info = CustomUser.objects.filter(id=request.user.id)[0]
        orders = OrderList.objects.all()
        centers_orders = []
        for i in FitnessCenter.objects.values('id', 'title'):
            centers_orders.append(
                {i.get('title'): OrderList.objects.filter(center_title=i.get('id')).count()}
            )
        return render(request, 'profile_admin.html', {'user': user_info, 'orders': orders,
                                                      'centers_orders': centers_orders})
    elif request.user.id is not None:
        user_info = CustomUser.objects.filter(id=request.user.id)[0]
        orders = OrderList.objects.filter(user=request.user)
        return render(request, 'profile.html', {'user': user_info, 'orders': orders})
    return render(request, 'register.html')
