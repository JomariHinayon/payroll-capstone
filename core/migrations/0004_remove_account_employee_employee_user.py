# Generated by Django 5.1.2 on 2024-10-28 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_employee_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='employee',
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
