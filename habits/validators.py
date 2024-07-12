from datetime import timedelta

from rest_framework import exceptions

from habits.models import Habit


class DurationValidator:
    """
    Кастомный валидатор, который проверяет, чтобы
    время выполнения было не больше 2 минут.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = value.get(self.field)
        if data is not None:
            if timedelta(minutes=data.minute) > timedelta(minutes=2):
                raise exceptions.ValidationError('Время выполнения должно быть не больше 2 минут')


class RelatedHabitValidator:
    """
    Кастомный валидатор, который проверяет,
    чтобы в связанные привычки могли попадать только привычки с признаком приятной привычки.
    А также, чтобы у приятной привычки не было связанной привычки.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = value.get(self.field)
        if data is not None:
            pleasant_habits = Habit.objects.filter(is_pleasant_habit=True)
            for pleasant_habit in pleasant_habits:
                if data != pleasant_habit:
                    raise exceptions.ValidationError('В связанные привычки могут попадать '
                                                     'только привычки с признаком приятной привычки.')
            raise exceptions.ValidationError('У приятной привычки не может быть связанной привычки.')


class AwardValidator:
    """
    Кастомный валидатор, который проверяет,
    чтобы у приятной привычки не было вознаграждения.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = value.get(self.field)
        if data is not None:
            raise exceptions.ValidationError('У приятной привычки не может быть вознаграждения')


class FrequencyValidator:
    """
    Кастомный валидатор, который проверяет, чтобы
    нельзя было выполнять привычку реже, чем 1 раз в 7 дней и более 7 дней.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        data = value.get(self.field)
        if data is None:
            if data != 'daily':
                raise exceptions.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')
            elif data != 'once_a_week':
                raise exceptions.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')
