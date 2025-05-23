# Generated by Django 5.0 on 2025-03-29 19:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('split', '0029_settlement_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupbalance',
            options={'ordering': ['-modified', '-group__modified'], 'verbose_name': 'Group Balance', 'verbose_name_plural': 'Group Balance'},
        ),
        migrations.AddField(
            model_name='split',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='split',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
