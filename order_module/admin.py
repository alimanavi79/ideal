from django.contrib import admin
from .models import Order, OrderDetail,User

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1
    fields = ['product', 'count', 'final_price']
    readonly_fields = ['final_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','id','user_address', 'is_paid', 'payment_date', 'status', 'created_at', 'calculate_total_price', 'calculate_total_quantity']
    list_filter = ['is_paid', 'payment_date', 'status', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_editable = ['status']
    inlines = [OrderDetailInline]

    def user_address(self, obj):
        return f"{obj.user.street}, {obj.user.postal_code}"
    user_address.short_description = 'آدرس کاربر'

    def calculate_total_price(self, obj):
        return obj.calculate_total_price()
    calculate_total_price.short_description = 'قیمت نهایی'

    def calculate_total_quantity(self, obj):
        return obj.calculate_total_quantity()
    calculate_total_quantity.short_description = 'کل محصولاتط   '


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'count', 'final_price']
    search_fields = ['order__user__username', 'product__name']
