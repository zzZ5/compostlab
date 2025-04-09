# Generated by Django 3.0.8 on 2025-04-09 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0007_auto_20241216_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='type',
            field=models.CharField(choices=[('RE', 'Reactor'), ('CP', 'Compass')], default='RE', max_length=32),
        ),
    ]
