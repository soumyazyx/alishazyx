# Generated by Django 3.0.4 on 2020-07-14 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0018_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
    ]
