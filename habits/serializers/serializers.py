from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabbitsPleasantValidator, RelatedIsOnlyPleasantHabitsValidator, TimeValidator


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'
        validators = [
            HabbitsPleasantValidator(fields),
            RelatedIsOnlyPleasantHabitsValidator(fields),
            TimeValidator(field='lead_time')
        ]


class HabitsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        # fields = '__all__'
        exclude = ("user",)
