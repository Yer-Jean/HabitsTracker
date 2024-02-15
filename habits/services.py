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


def send_reminder_to_user(chat_id, message):
    """Отправка напоминания пользователю в Telegram"""
    api_telegram = f'https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(api_telegram, data=params)
    if response.status_code == 200:
        print('Напоминание успешно отправлено в Telegram!')
    else:
        print('Ошибка при отправке напоминания в Telegram:', response.text)



