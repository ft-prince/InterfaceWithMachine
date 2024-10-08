# Generated by Django 5.0.6 on 2024-08-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0044_alter_fixturecleaningrecord_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fixturecleaningrecord",
            name="operator_signature",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK"), ("", "Not Checked")],
                default="✔",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="fixturecleaningrecord",
            name="supervisor_signature",
            field=models.CharField(
                blank=True,
                choices=[("✔", "OK"), ("✘", "Not OK"), ("", "Not Checked")],
                default="✘",
                max_length=1,
            ),
        ),
    ]
