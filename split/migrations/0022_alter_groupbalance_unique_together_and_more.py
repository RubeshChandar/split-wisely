# Generated by Django 5.0 on 2025-03-18 17:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("split", "0021_alter_groupbalance_group_alter_groupbalance_user"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="groupbalance",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="split",
            unique_together=set(),
        ),
    ]
