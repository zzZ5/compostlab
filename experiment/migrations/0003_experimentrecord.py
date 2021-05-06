# Generated by Django 3.0.8 on 2021-05-06 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiment', '0002_auto_20210429_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(blank=True, max_length=256)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('experiment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experimentrecord', to='experiment.Experiment')),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ExperimentRecord',
                'verbose_name_plural': 'ExperimentRecords',
                'db_table': 'experiment_record',
                'ordering': ['-created_time'],
            },
        ),
    ]