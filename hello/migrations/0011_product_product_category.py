# Generated by Django 3.0.4 on 2020-07-12 11:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("hello", "0010_auto_20200712_1646"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="product_category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="hello.Category",
            ),
            preserve_default=False,
        ),
    ]
