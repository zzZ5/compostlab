# Generated by Django 3.0.8 on 2024-12-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0006_auto_20241216_2141'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='equipment',
            index=models.Index(fields=['type'], name='equipment_type_839ba1_idx'),
        ),
        migrations.AddIndex(
            model_name='equipment',
            index=models.Index(fields=['created_time'], name='equipment_created_5cd3e2_idx'),
        ),
    ]
