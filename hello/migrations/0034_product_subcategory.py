# Generated by Django 3.0.4 on 2020-07-31 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0033_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
