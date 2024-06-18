from django.contrib import admin
from .models import Order, OrderDetail,User
from django.http import HttpResponse
from openpyxl import Workbook


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
        return f"{obj.user.ostan} - {obj.user.shahrestan} - {obj.user.street} - {obj.user.postal_code}"
    user_address.short_description = 'آدرس کاربر'

    def calculate_total_price(self, obj):
        return obj.calculate_total_price()
    calculate_total_price.short_description = 'قیمت نهایی'

    def calculate_total_quantity(self, obj):
        return obj.calculate_total_quantity()
    calculate_total_quantity.short_description = 'کل محصولاتط'

    # تابع برای ایجاد خروجی Excel
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'

        # ایجاد یک کتاب کار با استفاده از openpyxl
        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"

        # ساخت سرستون‌ها
        ws.append(['شناسه', 'آدرس کاربر', 'وضعیت', 'تاریخ پرداخت', 'قیمت نهایی'])

        # افزودن داده‌ها
        for order in queryset:
            ws.append([order.id, f"{order.user.ostan}, {order.user.shahrestan}, {order.user.street}, {order.user.postal_code}", order.status, order.payment_date, order.calculate_total_price()])

        # ذخیره فایل
        wb.save(response)
        return response
    
    export_to_excel.short_description = "خروجی Excel گرفتن"

    # اضافه کردن عملیات به پنل مدیریت
    actions = ['export_to_excel']

    


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'count', 'final_price']
    search_fields = ['order__user__username', 'product__name']
