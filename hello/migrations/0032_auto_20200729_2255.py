# Generated by Django 3.0.4 on 2020-07-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0031_auto_20200724_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]