# Generated by Django 3.0.4 on 2020-07-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_auto_20200712_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_sku',
            field=models.CharField(blank=True, default='-1', max_length=255),
        ),
    ]