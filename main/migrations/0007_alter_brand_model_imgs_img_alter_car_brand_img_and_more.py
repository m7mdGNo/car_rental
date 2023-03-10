# Generated by Django 4.1.6 on 2023-02-14 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_blog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand_model_imgs",
            name="img",
            field=models.ImageField(default="placeholder.png", upload_to=""),
        ),
        migrations.AlterField(
            model_name="car_brand",
            name="img",
            field=models.ImageField(default="placeholder.png", upload_to=""),
        ),
        migrations.AlterField(
            model_name="car_imgs",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="main.car",
            ),
        ),
        migrations.AlterField(
            model_name="car_imgs",
            name="img",
            field=models.ImageField(default="placeholder.png", upload_to=""),
        ),
    ]
