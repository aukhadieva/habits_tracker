import requests

from config import settings


def send_message(text, chat_id):
    """
    Сервисная функция по отправке сообщений телеграм-ботом.
    """
    params = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.get(f"{settings.TG_URL}{settings.TGBOT_TOKEN}/sendMessage", params=params)
