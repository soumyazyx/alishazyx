# Generated by Django 3.0.4 on 2020-08-01 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_telegrammessage_from_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrammessage',
            name='processing_status',
            field=models.CharField(default='NEW', max_length=255),
        ),
    ]
