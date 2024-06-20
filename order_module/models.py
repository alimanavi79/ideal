from django.db import models
from account_module.models import User
from product_module.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from product_module.models import DiscountCode



class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
        ('returned', 'مرجوع شده')

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده', default=False)
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing', verbose_name='وضعیت سفارش')
    tracking_code = models.IntegerField(verbose_name='کد رهگیری', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کد تخفیف')

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
    
    def calculate_total_price(self):
        total_amount = sum([detail.get_total_price() for detail in self.orderdetail_set.all()])
        if self.discount_code:
            discount_amount = (total_amount * self.discount_code.discount_percentage) / 100
            total_amount -= discount_amount
        return total_amount
    
    def calculate_total_price_without_discount(self):
        total_amount = sum([detail.get_total_price() for detail in self.orderdetail_set.all()])
        return total_amount

    def calculate_total_quantity(self):
        total_quantity = sum([detail.count for detail in self.orderdetail_set.all()])
        return total_quantity
    
    def get_status_display_farsi(self):
        return dict(self.STATUS_CHOICES).get(self.status)

                
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تعداد محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        if self.product.discounted_price is None:
            return self.count * self.product.price
        elif self.product.discounted_price < self.product.price:
            return self.count * self.product.discounted_price
        else:
            return self.count * self.product.price
        
    def __str__(self):
        return f"{self.product} ({self.count})"

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'

@receiver([post_save, post_delete], sender=OrderDetail)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total_price = order.calculate_total_price()
    total_quantity = order.calculate_total_quantity()
    order.save()
