# Generated by Django 3.0.4 on 2020-07-12 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_imggal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('category_desc', models.TextField(blank=True)),
            ],
        ),
    ]
