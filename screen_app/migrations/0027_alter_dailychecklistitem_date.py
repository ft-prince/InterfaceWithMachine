# Generated by Django 5.0.6 on 2024-07-22 10:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0026_dailychecklistitem_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
