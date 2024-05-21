from django.contrib.auth.models import AbstractUser
from django.db import models
from iranian_cities.models import Ostan, Shahrestan



# Create your models here.

class User(AbstractUser):
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')
    phone_number = models.CharField(max_length=20, verbose_name='شماره تلفن', null=True, blank=True)
    ostan = models.ForeignKey(Ostan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='استان')
    shahrestan = models.ForeignKey(Shahrestan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شهر')
    street = models.CharField(max_length=100, verbose_name='کوچه', null=True, blank=True)
    postal_code = models.CharField(max_length=20, verbose_name='پلاک', null=True, blank=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.email
 


