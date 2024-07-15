import datetime

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name="Пользователь", **NULLABLE
    )
    behavior = models.CharField(
        max_length=200,
        verbose_name="Действие",
        db_comment="действие, которое представляет собой привычка",
    )
    time = models.DateTimeField(
        verbose_name="Время", db_comment="дата старта и время, когда необходимо выполнять привычку"
    )
    location = models.CharField(max_length=200, verbose_name="Место")

    related_habit = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        **NULLABLE,
    )
    frequency = models.SmallIntegerField(
        default=1,
        verbose_name="Периодичность",
        db_comment="периодичность выполнения привычки для напоминания в днях",
        **NULLABLE,
    )
    award = models.CharField(max_length=200, verbose_name="Вознаграждение", **NULLABLE)
    duration = models.TimeField(
        verbose_name="Время на выполнение",
        default=datetime.time(00, 2, 00),
        db_comment="время, которое предположительно потратит пользователь на выполнение "
        "привычки",
        **NULLABLE,
    )

    is_pleasant_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    is_public = models.BooleanField(verbose_name="Признак публичности", **NULLABLE)

    def __str__(self):
        return f"привычку {self.behavior}, в {self.time} (локация: {self.location})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = (
            "is_pleasant_habit",
            "is_public",
        )
