from django.contrib import admin
from .models import Order, OrderDetail,User
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1
    fields = ['product', 'count', 'final_price']
    readonly_fields = ['final_price']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','id','user_address', 'is_paid', 'payment_date', 'status', 'created_at', 'calculate_total_price', 'calculate_total_quantity']
    list_filter = ['is_paid', ("payment_date", DateRangeQuickSelectListFilterBuilder()), 'status', 'created_at']
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

    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Orders"

        ws.append(['شناسه', 'آدرس کاربر', 'نام کاربر', 'شماره تماس', 'وضعیت', 'تاریخ پرداخت', 'محصول', 'تعداد', 'قیمت  کل خریداری شده'])

        for order in queryset:
            order_data = [
                order.id,
                f"{order.user.ostan}, {order.user.shahrestan}, {order.user.street}, {order.user.postal_code}",
                f"{order.user.first_name},{order.user.last_name}",
                order.user.phone_number,
                order.status,
                order.payment_date,
                "",  # محصول
                "",  # تعداد
                "",  # قیمت خریداری شده
            ]

            order_details = OrderDetail.objects.filter(order=order)

            for detail in order_details:
                if detail == order_details.first():
                    order_data[6] = detail.product.title
                    order_data[7] = detail.count
                    order_data[8] = detail.final_price
                    ws.append(order_data.copy())
                else:
                    ws.append(["", "", "", "", "", "", detail.product.title, detail.count, detail.final_price])

            ws.append(['', '', '', '', '', '', '', 'فروش کل:', order.calculate_total_price()])

        wb.save(response)
        return response
    
    export_to_excel.short_description = "خروجی Excel گرفتن"

    actions = ['export_to_excel']

    


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'count', 'final_price']
    search_fields = ['order__user__username', 'product__name']
