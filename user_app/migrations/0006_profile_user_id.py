# Generated by Django 5.1 on 2024-09-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_app", "0005_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="user_Id",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
