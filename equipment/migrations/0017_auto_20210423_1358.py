# Generated by Django 3.0.8 on 2021-04-23 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0016_auto_20210423_0822'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentRecordUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'EquipmentUsageRecord',
                'verbose_name_plural': 'EquipmentUsageRecords',
                'db_table': 'equipment_record_usage',
                'ordering': ['-created_time'],
            },
        ),
        migrations.RenameModel(
            old_name='EquipmentModifyRecord',
            new_name='EquipmentRecordModify',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='sensorrecord',
            name='modifier',
        ),
        migrations.RemoveField(
            model_name='sensorrecord',
            name='sensor',
        ),
        migrations.AlterModelTable(
            name='equipment',
            table='equipment',
        ),
        migrations.AlterModelTable(
            name='equipmentrecordmodify',
            table='equipment_record_modify',
        ),
        migrations.DeleteModel(
            name='EquipmentUsageRecord',
        ),
        migrations.DeleteModel(
            name='Sensor',
        ),
        migrations.DeleteModel(
            name='SensorRecord',
        ),
        migrations.AddField(
            model_name='equipmentrecordusage',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.Equipment'),
        ),
        migrations.AddField(
            model_name='equipmentrecordusage',
            name='users',
            field=models.ManyToManyField(related_name='equipmentrecordusage_used', to=settings.AUTH_USER_MODEL),
        ),
    ]
