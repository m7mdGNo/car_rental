# Generated by Django 4.1.6 on 2023-02-25 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0025_alter_carreview_car"),
    ]

    operations = [
        migrations.AddField(
            model_name="carreview",
            name="added_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 2, 25, 15, 5, 44, 871108, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
    ]