from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
# Register your models here.

# admin.site.register(models.User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # اضافه کردن تابع display_user_orders به نمایش

    def display_user_orders(self, obj):
        return obj.display_user_orders()

    display_user_orders.short_description = 'سفارش‌ها'

admin.site.register(User, UserAdmin)