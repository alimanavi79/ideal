from django.db import models
from account_module.models import User
from product_module.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils import timezone

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

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def calculate_total_price(self):
        total_amount = sum([detail.final_price if detail.final_price else detail.get_total_price() for detail in self.orderdetail_set.all()])
        return total_amount

    def calculate_total_quantity(self):
        total_quantity = sum([detail.count for detail in self.orderdetail_set.all()])
        return total_quantity
                
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return f"{self.product} ({self.count})"

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'

@receiver(post_save, sender=OrderDetail)
def update_final_price(sender, instance, **kwargs):
    if not instance.final_price:
        instance.final_price = instance.get_total_price()
        instance.save()
