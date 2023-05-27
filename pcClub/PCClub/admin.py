from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from PCClub.models import CustomUser
from .models import *
from .forms import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'phone_number',
                    'profile_image'
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
                    'phone_number',
                    'profile_image'
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)


class TariffsAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'device')
    list_display_links = ('title', )
    search_fields = ('title', 'cost', 'device')


admin.site.register(Tariff, TariffsAdmin)


class ClubsAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')
    filter_horizontal = ['tariffs']
    list_display_links = ('title', )
    search_fields = ('title', 'manager_phone')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Clubs, ClubsAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'club', 'tariff', 'cost')
    list_display_links = ('user', 'date')
    search_fields = ('date', 'user')


admin.site.register(Orders, OrdersAdmin)

