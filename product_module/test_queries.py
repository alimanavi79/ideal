from django.db import connection
from product_module.models import Product  # فرضاً نام مدل شما Product است

# ایجاد یک شیء از مدل
product = Product.objects.get(id=1)  # فرضاً اینجا از یک شیء موجود استفاده می‌کنیم

# فراخوانی متد save()
product.save()

# دریافت و چاپ دستورات SQL
queries = connection.queries
for query in queries:
    print(query['sql'])
