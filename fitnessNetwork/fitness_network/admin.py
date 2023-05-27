from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from fitness_network.models import CustomUser
from .models import *
from .forms import *


class FitnessCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contract_number', 'location')
    list_display_links = ('title', 'contract_number')
    search_fields = ('title', 'contract_number')


admin.site.register(FitnessCenter, FitnessCenterAdmin)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'activity', 'work_center')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Employer, EmployerAdmin)


class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'description', 'article')
    list_display_links = ('title', 'article')
    search_fields = ('title', 'article')


admin.site.register(Activities, ActivitiesAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'center_title', 'activity', 'date', 'order_date')
    list_display_links = ('user', 'order_date')
    search_fields = ('order_date', 'user')


admin.site.register(OrderList, OrderAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'full_name',
                    'phone_number'
                )
            }
        )
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'full_name',
                    'phone_number'
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
