# Generated by Django 3.0.8 on 2024-12-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0007_auto_20241216_2132'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='experiment',
            index=models.Index(fields=['status'], name='experiment_status_cf123b_idx'),
        ),
        migrations.AddIndex(
            model_name='experiment',
            index=models.Index(fields=['created_time'], name='experiment_created_5e12ec_idx'),
        ),
    ]