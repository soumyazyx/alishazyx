# Generated by Django 3.0.4 on 2020-07-17 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0025_auto_20200718_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desription',
            new_name='description',
        ),
    ]
