# # order_module/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order, OrderDetail, Product

# @receiver(post_save, sender=Order)
# def update_product_inventory(sender, instance, **kwargs):
#     if instance.is_paid:
#         order_details = instance.orderdetail_set.all()
#         for detail in order_details:
#             product = detail.product
#             if product.inventory >= detail.count:
#                 product.inventory -= detail.count
#                 product.save()
#             else:
#                 # اگر موجودی کافی نیست، می‌توانید از اینجا مدیریت کنید.
#                 # برای مثال می‌توانید یک ارور لاگ کنید یا عملیات دیگری انجام دهید.
#                 raise ValueError(f"Not enough inventory for product {product.title}")
