# Generated by Django 5.0.2 on 2024-02-09 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[("RUNNING", "Running"), ("STOPPED", "Stopped")],
                        default="STOPPED",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Screen",
            fields=[
                ("screen_id", models.AutoField(primary_key=True, serialize=False)),
                ("video_url", models.URLField()),
                ("pdf_url", models.URLField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="screen_app.product",
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="screen_app.station",
                    ),
                ),
            ],
        ),
    ]
