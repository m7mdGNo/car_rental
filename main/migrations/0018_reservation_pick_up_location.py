# Generated by Django 4.1.6 on 2023-02-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0017_reservation_end_date_reservation_start_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="pick_up_location",
            field=models.CharField(default="city", max_length=100),
            preserve_default=False,
        ),
    ]
