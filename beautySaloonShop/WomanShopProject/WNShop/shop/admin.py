from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import UserCreationForm, AdminUserChangeForm
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):

    form = AdminUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Права', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'available', 'created', 'uploaded')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'file')
    list_display_links = ('date', 'file')
    search_fields = ('user', 'file')


admin.site.register(Orders, OrderAdmin)