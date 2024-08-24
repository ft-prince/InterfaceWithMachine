# Generated by Django 5.1 on 2024-08-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0070_alter_startupchecksheet_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlychecklistitem",
            name="check_point_12",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "Check Machine Earthing (Leakage Voltage)",
                        "Check Machine Earthing (Leakage Voltage)",
                    ),
                    ("Check all parameter", "Check all parameter"),
                    ("Check Working condition", "Check Working condition"),
                    ("Check Operation of Sensors", "Check Operation of Sensors"),
                    (
                        "Check condition of all fixture",
                        "Check condition of all fixture",
                    ),
                ],
                default="Check Machine Earthing (Leakage Voltage)",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="monthlychecklistitem",
            name="method_of_checking_12",
            field=models.CharField(
                blank=True,
                choices=[
                    ("By Parameter", "By Parameter"),
                    ("By Condition", "By Condition"),
                    ("By Condition", "By Condition"),
                    ("By Fixture", "By Fixture"),
                ],
                default="By Parameter",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="monthlychecklistitem",
            name="requirement_range_12",
            field=models.CharField(
                blank=True,
                choices=[
                    ("< 2 V", "< 2 V"),
                    ("Condition Proper", "Condition Proper"),
                    ("Condition Proper", "Condition Proper"),
                    ("Proper Condition", "Proper Condition"),
                ],
                default="< 2 V",
                max_length=200,
            ),
        ),
    ]
