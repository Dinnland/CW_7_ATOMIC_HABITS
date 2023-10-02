from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabitsPleasantValidator, RelatedIsOnlyPleasantHabitsValidator, TimeValidator


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'
        validators = [
            HabitsPleasantValidator(fields),
            RelatedIsOnlyPleasantHabitsValidator(fields),
            TimeValidator(field='lead_time')
        ]


