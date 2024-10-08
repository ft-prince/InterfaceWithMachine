# Generated by Django 5.0.6 on 2024-08-15 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0031_alter_dailychecklistitem_checked_by_operator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_1",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Clean Machine Surface",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_2",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check ON/OFF Switch",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_3",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check Emergency Switch",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_4",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check any Abnormal Sound in M/C",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_5",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check Spray Nozzle",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_6",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check all Tubbing & Feeder pipe",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="check_point_7",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Clean Machine Surface", "Clean Machine Surface"),
                    ("Check ON/OFF Switch", "Check ON/OFF Switch"),
                    ("Check Emergency Switch", "Check Emergency Switch"),
                    (
                        "Check any Abnormal Sound in M/C",
                        "Check any Abnormal Sound in M/C",
                    ),
                    ("Check Spray Nozzle", "Check Spray Nozzle"),
                    (
                        "Check all Tubbing & Feeder pipe",
                        "Check all Tubbing & Feeder pipe",
                    ),
                    (
                        "Check Maintenance & Calibration Tag",
                        "Check Maintenance & Calibration Tag",
                    ),
                ],
                default="Check Maintenance & Calibration Tag",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_1",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="Proper Clean",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_2",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="Proper Working",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_3",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="Proper Working",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_4",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="No any Abnormal Sound",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_5",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="No Blockage No leakage",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_6",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="No Cut & No Damage",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="requirement_range_7",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Proper Clean", "Proper Clean"),
                    ("Proper Working", "Proper Working"),
                    ("Proper Working", "Proper Working"),
                    ("No any Abnormal Sound", "No any Abnormal Sound"),
                    ("No Blockage No leakage", "No Blockage No leakage"),
                    ("No Cut & No Damage", "No Cut & No Damage"),
                    ("No Expiry date on tag", "No Expiry date on tag"),
                ],
                default="No Expiry date on tag",
                max_length=200,
            ),
        ),
    ]
