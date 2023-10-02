from django.contrib import admin

from habits.models import Habits


# Register your models here.

@admin.register(Habits)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'time', 'action',
                    'is_pleasant_habit',
                    'related_habit', 'periodicity', 'reward', 'lead_time',
                    'is_published',)
