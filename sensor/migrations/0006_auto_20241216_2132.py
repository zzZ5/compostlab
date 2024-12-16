# Generated by Django 3.0.8 on 2024-12-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0005_sensor_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='type',
            field=models.CharField(choices=[('T', 'Temperature Sensor'), ('H', 'Humidity Sensor'), ('CO2', 'CO2 Sensor')], default='T', max_length=32),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='unit',
            field=models.CharField(choices=[('℃', 'Celsius'), ('%', 'Percent'), ('ppm', 'ppm')], default='℃', max_length=32),
        ),
        migrations.AlterField(
            model_name='sensorrecord',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
