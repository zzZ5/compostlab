# Generated by Django 3.0.8 on 2021-04-16 23:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0007_auto_20210416_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='users',
            field=models.ManyToManyField(related_name='equipment_inuse', to=settings.AUTH_USER_MODEL),
        ),
    ]
