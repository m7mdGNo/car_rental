# Generated by Django 4.1.6 on 2023-02-20 04:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0019_car_accepted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reservation",
            name="payment_method",
        ),
    ]
