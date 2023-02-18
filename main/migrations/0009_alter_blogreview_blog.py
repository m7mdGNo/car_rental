# Generated by Django 4.1.6 on 2023-02-14 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_blogreview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogreview",
            name="blog",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="main.blog",
            ),
        ),
    ]
