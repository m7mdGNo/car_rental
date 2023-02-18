# Generated by Django 4.1.6 on 2023-02-15 07:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0014_alter_car_added_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="car",
            name="luggage",
        ),
        migrations.RemoveField(
            model_name="car",
            name="seats",
        ),
        migrations.AddField(
            model_name="brand_model",
            name="luggage",
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="brand_model",
            name="seats",
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
    ]
