# Generated by Django 5.0.6 on 2024-07-22 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0021_alter_dailychecklistitem_approved_by_supervisor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="approved_by_Supervisor",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK"), ("", "Not Checked")],
                default="✘",
                max_length=100,
            ),
        ),
    ]
