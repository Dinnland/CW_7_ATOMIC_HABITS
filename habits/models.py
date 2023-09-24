from django.conf import settings
from django.db import models
from django.utils.timezone import now

NULLABLE = {'null': True, 'blank': True}


class Habits(models.Model):
    """Привычки"""

    PERIODICITY_NAME = [
        (1, 'раз в день'),
        (2, 'раз в 2 дня'),
        (3, 'раз в 3 дня'),
        (4, 'раз в 4 дня'),
        (5, 'раз в 5 дней'),
        (6, 'раз в 6 дней'),
        (7, 'раз в 7 дней')
        #  мб дни недели еще
    ]
    # name = models.CharField(max_length=150, verbose_name='Название')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')
    place = models.CharField(max_length=150, verbose_name='Место')
    time = models.DateTimeField(default=now, verbose_name='Время / по умолч: сейчас')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной/доп. привычки')
    related_habit = models.ForeignKey("Habits", verbose_name='Связанная привычка',
                                      on_delete=models.CASCADE, **NULLABLE, related_name='habit')
    periodicity = models.PositiveSmallIntegerField(verbose_name='Периодичность',
                                                   default=1, choices=PERIODICITY_NAME)
    reward = models.TextField(verbose_name='Вознаграждение', **NULLABLE)
    lead_time = models.TimeField(verbose_name='Время выполнения')
    is_published = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        # ordering = ('',)
