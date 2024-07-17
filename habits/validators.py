import datetime

from rest_framework import exceptions

from habits.models import Habit


class AwardValidator:
    """
    Кастомный валидатор, который исключает
    одновременный выбор связанной привычки и указания вознаграждения.
    """

    def __init__(self, field, field2):
        self.field = field
        self.field2 = field2

    def __call__(self, value):
        award = dict(value).get(self.field)
        related_habit = dict(value).get(self.field2)
        if award and related_habit:
            raise exceptions.ValidationError(
                "Одновременный выбор связанной привычки и вознаграждения запрещен."
            )


class DurationValidator:
    """
    Кастомный валидатор, который проверяет, чтобы
    время выполнения было не больше 2 минут.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        habits_time = dict(value).get(self.field)
        if habits_time is not None:
            if habits_time > datetime.time(minute=2):
                raise exceptions.ValidationError(
                    "Время выполнения должно быть не больше 2 минут"
                )


class RelatedHabitValidator:
    """
    Кастомный валидатор, который проверяет,
    чтобы в связанные привычки могли попадать только привычки с признаком приятной привычки.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = dict(value).get(self.field)
        if related_habit is not None:
            if not Habit.objects.filter(
                related_habit=related_habit.is_pleasant_habit
            ).exists:
                raise exceptions.ValidationError(
                    "В связанные привычки могут попадать "
                    "только привычки с признаком приятной привычки."
                )


class IsPleasantHabitValidator:
    """
    Кастомный валидатор, который проверяет,
    чтобы у приятной привычки не было вознаграждения и связанной привычки.
    """

    def __init__(self, field, fild2, fild3):
        self.field = field
        self.field2 = fild2
        self.field3 = fild3

    def __call__(self, value):
        is_pleasant_habit = dict(value).get(self.field)
        award = dict(value).get(self.field2)
        related_habit = dict(value).get(self.field3)
        if is_pleasant_habit:
            if award is not None:
                raise exceptions.ValidationError(
                    "У приятной привычки не может быть вознаграждения."
                )
            if related_habit is not None:
                raise exceptions.ValidationError(
                    "У приятной привычки не может быть связанной привычки."
                )


class FrequencyValidator:
    """
    Кастомный валидатор, который проверяет, чтобы
    нельзя было выполнять привычку реже, чем 1 раз в 7 дней и более 7 дней.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        frequency = dict(value).get(self.field)
        if frequency is not None:
            if frequency > 7:
                raise exceptions.ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
                )
