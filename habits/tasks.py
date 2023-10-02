from datetime import datetime, timedelta

import requests
from django.conf import settings
from celery import shared_task

from habits.models import Habits
from users.models import User

telegram_bot_token = settings.TELEGRAM_API_KEY


@shared_task
def get_chat_id():
    """Получение и Добавление telegram_chat_id пользователям, с указанным в бд юзернейном телеги (telegram_username)"""
    response = requests.get(f'https://api.telegram.org/bot{telegram_bot_token}/getUpdates')
    chats = response.json()['result']
    users = User.objects.all()

    for the_user in users:
        if the_user.telegram_username:
            if not the_user.telegram_chat_id:
                for chat in chats:
                    print(chat['message']['from']['username'])
                    if chat['message']['from']['username']:
                        print(chat['message']['from']['username'])
                        if the_user.telegram_username == chat['message']['from']['username']:
                            the_user.telegram_chat_id = chat['message']['chat']['id']
                            the_user.save()


@shared_task
def send_telegram_message():
    """Отправка уведомления пользователю в телеграм"""
    time_now = datetime.now()
    habits = Habits.objects.filter(time__gte=time_now - timedelta(minutes=1)).filter(time__lte=time_now)
    for habit in habits:
        message = (f'Напоминание от Трекера привычек:'
                   f'Я - {habit.user.telegram_username}, буду {habit.action} в {habit.time} в {habit.place}')
        response = requests.get(
            f'https://api.telegram.org/bot{telegram_bot_token}'
            f'/sendMessage?chat_id={habit.user.telegram_chat_id}&text={message}')
        return response.json()

