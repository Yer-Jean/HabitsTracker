from datetime import timedelta, datetime
from math import ceil

import requests

from django.conf import settings


def get_chat_id(telegram_username):
    """Получение chat_id пользователя по его имени в телеграм"""

    api_telegram = f'https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getUpdates'
    response = requests.get(api_telegram)
    data = response.json()

    if data.get('ok', False):
        for result in data.get('result', []):
            message = result.get('message', {})
            if 'from' in message and 'username' in message['from']:
                if telegram_username[1:] == message['from']['username']:
                    return message['from']['id']
    return None


def rounded_datetime(date_time: datetime):
    """
    Метод возвращает дату и время, с количеством минут, округленных до кратного
    параметру CELERY_BEAT_PERIOD. В большую сторону, начиная от начала часа.

    Например: если CELERY_BEAT_PERIOD=19, а date_time=2023-10-16 15:33:00, то
    метод вернет значение 2023-10-16 15:38:00,
    или,
    если CELERY_BEAT_PERIOD=5, а date_time=2023-10-16 15:28:00, то
    метод вернет значение 2023-10-16 15:30:00.

    :param date_time: объект DateTime, который надо округлить
    :return: округленный объект DateTime
    """
    hours, minutes = divmod(ceil(date_time.minute / int(settings.CELERY_BEAT_PERIOD))
                            * int(settings.CELERY_BEAT_PERIOD), 60)
    return (date_time + timedelta(hours=hours)).replace(minute=minutes, second=0, microsecond=0)
