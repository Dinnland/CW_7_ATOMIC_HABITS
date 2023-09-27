from rest_framework import serializers
from rest_framework.serializers import ValidationError


class HabbitsPleasantValidator:
    """Проверка приятных полей"""

    def __init__(self, fields):
        self.fields = fields
        self.message = 'Поля конфликтуют друг с другом'

    def __call__(self, data):
        is_pleasant_habit = dict(data).get('is_pleasant_habit')
        related_habit = dict(data).get('related_habit')
        reward = dict(data).get('reward')

        if is_pleasant_habit:
            """Проверка: если это приятная привычка, то вознаграждения и связанной привычки не может быть"""
            if reward != None or related_habit != None:
                raise serializers.ValidationError({
                    'is_pleasant_habit': 'Вы указали: "is_pleasant_habit": true.'
                                         'Но у полезной привычки не может быть: reward, related_habit'
                })
        else:
            if reward != None and related_habit != None:
                """Проверка: вознаграждение и связанная привычка не могут быть одновременно"""

                raise serializers.ValidationError({
                    'reward_or_related_habit': 'У привычки не может быть одновременно: reward, related_habit'
                })


class RelatedIsOnlyPleasantHabitsValidator:
    """Проверка связанного поля на признак приятной привычки """
    def __init__(self, fields):
        self.fields = fields
        self.message = 'Выбранная привычка не имеет признака приятной привычки'

    def __call__(self, data):
        related_habit = dict(data).get('related_habit')
        if related_habit:
            if not related_habit.is_pleasant_habit:
                raise ValidationError(
                    {'related_is_only_pleasant_habit':
                         'Выбранная связанная/приятная привычка не имеет признака приятной привычки!'
                     })


class TimeValidator:
    """Время выполнения не должно быть больше 120 секунд"""

    def __init__(self, field):
        self.field = field
        self.message = 'Время выполнения не должно быть больше 120 секунд'

    def __call__(self, value):
        lead_time = dict(value).get(self.field)
        seconds = lead_time.hour * 3600 + lead_time.minute * 60 + lead_time.second
        if seconds > 120:
            raise ValidationError({'habit_execution_time_exceeded': 'Время выполнения не должно превышать 120 сек!'})
