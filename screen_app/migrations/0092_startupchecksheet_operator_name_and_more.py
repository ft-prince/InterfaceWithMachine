# Generated by Django 5.1 on 2024-08-28 18:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0091_dailychecklistitem_manager_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="startupchecksheet",
            name="operator_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="startupchecksheet",
            name="verified_by",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK")],
                default="✘",
                max_length=1,
            ),
        ),
    ]
