# Generated by Django 3.0.4 on 2020-07-17 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0021_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='iamge',
            field=models.ImageField(blank=True, upload_to='images/categories/'),
        ),
    ]
