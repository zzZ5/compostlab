# Generated by Django 3.0.8 on 2024-12-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userrecord_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecord',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
