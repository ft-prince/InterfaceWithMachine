# Generated by Django 5.0.6 on 2024-08-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0028_alter_dailychecklistitem_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="doc_number",
            field=models.CharField(blank=True, default="QSF-13-06", max_length=20),
        ),
    ]
