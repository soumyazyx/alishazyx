# Generated by Django 3.0.4 on 2020-08-01 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0035_auto_20200801_0140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('category', 'sequence', 'created_on'), 'verbose_name_plural': 'Sub-Categories'},
        ),
    ]
