# Generated by Django 3.0.4 on 2020-07-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20200712_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_sku',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_desription',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(max_length=255),
        ),
    ]
