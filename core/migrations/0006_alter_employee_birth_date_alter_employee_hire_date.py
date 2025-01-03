# Generated by Django 5.1.2 on 2024-10-31 13:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_payroll_salary_structure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='birth_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
