# Generated by Django 4.2.5 on 2023-09-28 04:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habits_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habits',
            name='time',
            field=models.TimeField(default=datetime.time(7, 59, 2, 413410), verbose_name='Время / по умолч: сейчас'),
        ),
    ]