# Generated by Django 3.0.8 on 2021-04-27 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0018_auto_20210423_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(blank=True, max_length=256)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'EquipmentRecord',
                'verbose_name_plural': 'EquipmentRecords',
                'db_table': 'equipment_record',
                'ordering': ['-created_time'],
            },
        ),
        migrations.RemoveField(
            model_name='equipmentrecordusage',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='equipmentrecordusage',
            name='users',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='begin_time',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='key',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='users',
        ),
        migrations.DeleteModel(
            name='EquipmentRecordModify',
        ),
        migrations.DeleteModel(
            name='EquipmentRecordUsage',
        ),
        migrations.AddField(
            model_name='equipmentrecord',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentrecord', to='equipment.Equipment'),
        ),
        migrations.AddField(
            model_name='equipmentrecord',
            name='modifier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
