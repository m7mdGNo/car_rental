# Generated by Django 4.1.6 on 2023-02-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_user_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="cart_pick_up_location",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]