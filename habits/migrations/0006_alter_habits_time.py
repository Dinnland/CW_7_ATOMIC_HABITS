# Generated by Django 4.2.5 on 2023-09-29 01:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_alter_habits_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habits',
            name='time',
            field=models.TimeField(default=datetime.time(4, 23, 18, 789934), verbose_name='Время / по умолч: сейчас'),
        ),
    ]
