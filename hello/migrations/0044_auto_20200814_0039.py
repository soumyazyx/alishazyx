# Generated by Django 3.0.4 on 2020-08-13 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0043_auto_20200814_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_1',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_2',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_3',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_4',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_5',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_6',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_7',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_8',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='additional_image_9',
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_1',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_2',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_3',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_4',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_5',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_6',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_7',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_8',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_image_9',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/'),
        ),
    ]
