# Generated by Django 3.0.8 on 2021-04-26 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0018_auto_20210423_1432'),
        ('data', '0002_auto_20210423_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='unit',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensor', to='equipment.Equipment'),
        ),
    ]
