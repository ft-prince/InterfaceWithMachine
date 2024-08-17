# Generated by Django 5.0.6 on 2024-08-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0052_solderingbitrecord_operator_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solderingbitrecord",
            name="approved_by",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK"), ("", "Not Checked")],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="solderingbitrecord",
            name="prepared_by",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK"), ("", "Not Checked")],
                max_length=100,
            ),
        ),
    ]
