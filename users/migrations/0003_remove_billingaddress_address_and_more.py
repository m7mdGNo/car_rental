# Generated by Django 4.1.6 on 2023-02-12 06:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_cartitem_unique_together_cartitem_car_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billingaddress",
            name="address",
        ),
        migrations.RemoveField(
            model_name="billingaddress",
            name="state",
        ),
    ]
