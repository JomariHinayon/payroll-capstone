# Generated by Django 5.1.2 on 2024-11-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_payroll_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='total_wage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='employee',
            name='daily_wage',
            field=models.DecimalField(decimal_places=2, default=500.0, max_digits=10),
        ),
    ]