# Generated by Django 5.0 on 2025-02-22 01:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("split", "0009_alter_groupbalance_balance"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="groupbalance",
            options={"verbose_name": "Group Balance"},
        ),
        migrations.AddField(
            model_name="groupbalance",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
