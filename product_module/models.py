from django.db import models
from django.urls import reverse
from account_module.models import User
from django.core.exceptions import ValidationError


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    discounted_price = models.IntegerField(verbose_name='قیمت با تخفیف', null=True, blank=True, default=None)
    inventory = models.IntegerField(verbose_name='موجودی', default=0)
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')


    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])
    
    def is_available(self, quantity=1):
        return self.inventory >= quantity

    def save(self, *args, **kwargs):
        if self.discounted_price and self.discounted_price < self.price:
            # If the discounted price is less than the original price, save it
            super().save(*args, **kwargs)
        elif self.discounted_price and self.discounted_price > self.price:
            # If the discounted price is greater than the original price, raise a ValidationError
            raise ValidationError("Discounted price cannot be greater than the original price.")
        else:
            # If there is no discounted price, save the object
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    # @classmethod
    # def custom_query(cls):
    #     # کوئری SQL سفارشی
    #     sql_query = "SELECT id, title, price FROM product_module_product WHERE price > 100 LIMIT 10"
        
    #     # اجرای کوئری و بازگردانی نتیجه به عنوان نمونه‌های شیء مدل
    #     return cls.objects.raw(sql_query)

    # def custom_save(self, *args, **kwargs):
    #     # انجام عملیات مورد نظر شما برای ذخیره
    #     pass  # اینجا کدهای خود را قرار دهید

    # def custom_update(self, *args, **kwargs):
    #     # انجام عملیات مورد نظر شما برای بروزرسانی
    #     pass  # اینجا کدهای خود را قرار دهید

    # def save(self, *args, **kwargs):
    #     # انجام عملیات دلخواه شما قبل از ذخیره
    #     # مثلاً اعتبارسنجی و یا ایجاد فیلدهای دیگر
    #     with connection.cursor() as cursor:
    #         cursor.callproc('your_save_procedure_name', [self.title, self.category, self.image, ...])  # فراخوانی store procedure برای ذخیره اطلاعات

    #     super().save(*args, **kwargs)  # فراخوانی متد save() پیش‌فرض

    #     # انجام عملیات دلخواه شما بعد از ذخیره
    #     # مثلاً ارسال ایمیل یا به‌روزرسانی داده‌های دیگر
    
    # def update(self, *args, **kwargs):
    #         with connection.cursor() as cursor:
    #             cursor.callproc('your_update_procedure_name', [self.id, self.title, self.category, self.image, ...])  # فراخوانی store procedure برای به‌روزرسانی اطلاعات


class SpecificationKey(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name='کلید')
    category = models.ForeignKey(ProductCategory, related_name='specification_keys', on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'کلید مشخصات'
        verbose_name_plural = 'کلیدهای مشخصات'

    def __str__(self):
        return self.key
    
class TechnicalSpecification(models.Model):
    product = models.ForeignKey(Product, related_name='technical_specifications', on_delete=models.CASCADE, verbose_name='محصول')
    key = models.ForeignKey(SpecificationKey, related_name='technical_specifications', on_delete=models.CASCADE, verbose_name='کلید')
    value = models.CharField(max_length=300, verbose_name='مقدار')

    class Meta:
        verbose_name = 'مشخصات فنی'
        verbose_name_plural = 'مشخصات فنی'

    def __str__(self):
        return f"{self.product.title} - {self.key.key}: {self.value}"


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'

from django.utils import timezone

class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')
    start_date = models.DateTimeField(verbose_name='زمان شروع')
    end_date = models.DateTimeField(verbose_name='زمان پایان')
    discount_percentage = models.IntegerField(verbose_name='درصد تخفیف')

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'