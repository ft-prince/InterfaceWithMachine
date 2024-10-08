# Generated by Django 5.1 on 2024-08-28 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0085_alter_solderingbitrecord_machine_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychecklistitem",
            name="machine_location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="screen_app.machinelocation",
                verbose_name="Process/Operation",
            ),
        ),
        migrations.AlterField(
            model_name="monthlychecklistitem",
            name="machine_location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="screen_app.machinelocation",
                verbose_name="Process/Operation",
            ),
        ),
        migrations.AlterField(
            model_name="solderingbitrecord",
            name="machine_no",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="screen_app.machinelocation",
                verbose_name="Process/Operation",
            ),
        ),
        migrations.AlterField(
            model_name="weeklychecklistitem",
            name="machine_location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="screen_app.machinelocation",
                verbose_name="Process/Operation",
            ),
        ),
    ]
