# Generated by Django 4.2.5 on 2023-09-29 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Телеграмм чат id'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_nickname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя в Телеграмм'),
        ),
    ]
