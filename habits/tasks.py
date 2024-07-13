import pytz
from celery import shared_task
from datetime import datetime

from config import settings
from habits.models import Habit
from habits.services import send_message


@shared_task
def send_reminder():
    """
    Периодическая задача для напоминания о том, в какое время
    и какие привычки необходимо выполнять.
    Также удаляет привычку, если прошло 7 напоминаний.
    """
    current_time = datetime.now(pytz.timezone(settings.TIME_ZONE)).time().strftime('%X')
    habits = Habit.objects.all()

    for habit in habits:
        if habit.time.strftime('%X') == current_time and habit.frequency > 0:
            text = (
                f'Итс тайм! Выполни "{habit.behavior}" в локации {habit.location} '
                f'и получи {habit.award if habit.award else (habit.related_habit if habit.related_habit
                                                             else "хорошее настроение")}!')

            chat_id = habit.owner.tg_chat_id
            send_message(text, chat_id)
            habit.frequency -= 1
            habit.save()
