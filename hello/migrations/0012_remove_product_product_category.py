# Generated by Django 3.0.4 on 2020-07-12 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0011_product_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_category',
        ),
    ]
