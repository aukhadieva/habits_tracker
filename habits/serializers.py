from rest_framework import serializers

from habits.models import Habit
from habits.validators import DurationValidator, RelatedHabitValidator, AwardValidator, FrequencyValidator


class HabitSerializers(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [DurationValidator(field='duration'), RelatedHabitValidator(field='related_habit'),
                      AwardValidator(field='award'), FrequencyValidator(field='frequency')]
