# Generated by Django 5.0 on 2025-03-26 16:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('split', '0025_alter_groupbalance_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Settle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settle_pb', to=settings.AUTH_USER_MODEL)),
                ('paid_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settle_pt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
