# Generated by Django 5.1 on 2024-08-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0077_alter_rejectionsheet_part_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MachineLocation",
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
                (
                    "location_name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Machine Location"
                    ),
                ),
                (
                    "min_skill_required",
                    models.IntegerField(verbose_name="Minimum Skill Required"),
                ),
            ],
        ),
    ]
