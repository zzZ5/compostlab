# Generated by Django 3.2.3 on 2021-07-06 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_remove_data_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='measured_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]