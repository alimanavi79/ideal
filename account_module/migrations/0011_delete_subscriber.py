# Generated by Django 4.2.13 on 2024-06-19 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0010_subscriber'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]