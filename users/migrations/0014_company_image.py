# Generated by Django 4.1.6 on 2023-03-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_remove_company_email_remove_company_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="image",
            field=models.ImageField(default="profile.png", upload_to=""),
        ),
    ]
