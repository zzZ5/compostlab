# Generated by Django 3.2.3 on 2021-05-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0004_auto_20210510_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='status',
            field=models.IntegerField(choices=[(-1, 'Failed'), (1, 'Doing'), (2, 'Done'), (0, 'Applying')], default=0),
        ),
    ]