from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_doctor')
    list_filter = ('is_doctor',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'name', 'password')}),
        ('Права', {'fields': ('is_doctor', 'is_admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost')
    list_display_links = ('title',)
    search_fields = ('cost', 'title')


admin.site.register(Services, ServicesAdmin)


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_fields = ('user',)

    filter_horizontal = ['services']


admin.site.register(Doctors, DoctorsAdmin)


class ReceptionsAdmin(admin.ModelAdmin):
    list_display = ('date', 'client', 'doctor', 'service')
    list_display_links = ('date', )
    search_fields = ('date',)


admin.site.register(Receptions, ReceptionsAdmin)