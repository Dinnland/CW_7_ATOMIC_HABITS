# Generated by Django 4.2.5 on 2023-10-01 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0007_alter_habits_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habits',
            name='time',
            field=models.TimeField(default=datetime.time(1, 52, 1, 10967), verbose_name='Время / по умолч: сейчас'),
        ),
    ]
