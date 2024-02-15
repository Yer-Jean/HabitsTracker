import logging
import requests
from datetime import datetime
from celery import shared_task
from django.conf import settings

from habits.models import Habit
from habits.services import rounded_datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def check_habits_reminder():
    """Проверка привычек и отправка напоминаний пользователям"""
    current_day = datetime.now().weekday()
    rounded_datetime_now = rounded_datetime(datetime.now())

    habits = Habit.objects.filter(time=rounded_datetime_now)
    for habit in habits:
        logger.info(f"Processing habit: {habit.action}")
        if habit.owner and habit.owner.telegram_chat_id:
            # Если привычка ежедневная или сегодня день, указанный в периодичности
            if habit.periodicity == '0' or int(habit.periodicity) == current_day:
                message = f"Time to do the habit: {habit.action}"
                # Асинхронно отправляем сообщение в Телеграм
                send_reminder_to_user.delay(habit.owner.telegram_chat_id, message)


@shared_task
def send_reminder_to_user(chat_id, message):
    """Отправка напоминания пользователю в Telegram"""
    api_telegram = f'https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(api_telegram, data=params)
    if response.status_code == 200:
        logger.info('Reminder successfully sent to Telegram!')
    else:
        logger.info(f'Error when sending reminders in Telegram: {response.text}')
