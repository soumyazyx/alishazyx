# Generated by Django 3.0.4 on 2020-08-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0038_auto_20200813_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover_img_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img_urls_csv',
            field=models.TextField(blank=True, null=True),
        ),
    ]
