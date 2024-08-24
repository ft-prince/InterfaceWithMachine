# Generated by Django 5.1 on 2024-08-24 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0072_defects_rejectionsheet_defects"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rejectionsheet",
            name="defects",
        ),
        migrations.AddField(
            model_name="rejectionsheet",
            name="defects",
            field=models.ManyToManyField(
                blank=True, null=True, to="screen_app.defects"
            ),
        ),
    ]
