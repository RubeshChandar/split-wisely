# Generated by Django 5.0 on 2025-03-12 00:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("split", "0018_alter_groupbalance_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupbalance",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
