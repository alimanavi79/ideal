# Generated by Django 3.2.8 on 2024-06-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0005_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'در حال پردازش'), ('shipped', 'ارسال شده'), ('delivered', 'تحویل داده شده'), ('cancelled', 'لغو شده'), ('returned', 'مرجوع شده')], default='processing', max_length=10, verbose_name='وضعیت سفارش'),
        ),
    ]
