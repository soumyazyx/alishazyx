# Generated by Django 3.0.4 on 2020-07-12 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0014_auto_20200712_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_created_on',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category_last_modified',
            new_name='last_modified',
        ),
    ]