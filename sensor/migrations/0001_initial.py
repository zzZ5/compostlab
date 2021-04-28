# Generated by Django 3.0.8 on 2021-04-28 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('name_brief', models.CharField(max_length=64, null=True)),
                ('key', models.CharField(max_length=16, null=True, unique=True)),
                ('type', models.CharField(choices=[('T', 'Temperature sensor'), ('H', 'Humidity sensor')], default='T', max_length=32)),
                ('descript', models.CharField(max_length=256, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors', to='equipment.Equipment')),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensors',
                'db_table': 'sensor',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='SensorRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(blank=True, max_length=256)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sensor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sensorrecord', to='sensor.Sensor')),
            ],
            options={
                'verbose_name': 'SensorRecord',
                'verbose_name_plural': 'SensorRecords',
                'db_table': 'sensor_record',
                'ordering': ['-created_time'],
            },
        ),
    ]
