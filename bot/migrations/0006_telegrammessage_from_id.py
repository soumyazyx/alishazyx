# Generated by Django 3.0.4 on 2020-07-31 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20200729_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrammessage',
            name='from_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
