# Generated by Django 3.0.8 on 2021-04-16 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0006_auto_20210416_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='user',
            new_name='users',
        ),
    ]
