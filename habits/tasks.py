from datetime import datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_reminder_to_user


@shared_task
def check_habits_reminder():
    """Проверка привычек и отправка напоминаний пользователям"""
    current_day = datetime.now().weekday()
    habits = Habit.objects.filter(time__lte=datetime.now())
    for habit in habits:
        if habit.owner and habit.owner.telegram_chat_id:
            # Если привычка ежедневная или сегодня день, указанный в периодичности
            if habit.periodicity == '0' or int(habit.periodicity) == current_day:
                message = f"Время выполнить привычку: {habit.action}"
                send_reminder_to_user(habit.owner.telegram_chat_id, message)