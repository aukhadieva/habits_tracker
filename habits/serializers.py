from rest_framework import serializers

from habits.models import Habit
from habits.validators import (AwardValidator, DurationValidator, RelatedHabitValidator,
                               IsPleasantHabitValidator, FrequencyValidator)


class HabitSerializers(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [AwardValidator(field='award', field2='related_habit'), DurationValidator(field='duration'),
                      RelatedHabitValidator(field='related_habit'),
                      IsPleasantHabitValidator(field='is_pleasant_habit', fild2='award', fild3='related_habit'),
                      FrequencyValidator(field='frequency')]
