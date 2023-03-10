# Generated by Django 4.1.6 on 2023-03-01 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_company_image"),
        ("main", "0031_car_visits"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cars",
                to="users.company",
            ),
        ),
    ]
