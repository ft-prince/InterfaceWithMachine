# Generated by Django 5.0.6 on 2024-08-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0035_alter_dailychecklistitem_station"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="station",
            field=models.CharField(
                choices=[
                    ("DSL01_S01", "DSL01_S01"),
                    ("DSL01_S02", "DSL01_S02"),
                    ("DSL01_S03", "DSL01_S03"),
                    ("DSL01_S04", "DSL01_S04"),
                    ("DSL01_S05", "DSL01_S05"),
                    ("DSL01_S06", "DSL01_S06"),
                    ("DSL01_S07", "DSL01_S07"),
                    ("DSL01_S08", "DSL01_S08"),
                    ("DSL01_S09", "DSL01_S09"),
                ],
                default=None,
                max_length=10,
            ),
        ),
    ]
