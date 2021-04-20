"""Функции для работы с датой и временем."""
from datetime import time

import pytz


def get_tzinfo():
    """Таймзона бота.

    Returns:
        Таймзона.
    """
    return pytz.timezone('Europe/Moscow')


def make_time(hour, minutes):
    """Сбор объекта времени.

    Parameters:
        hour: Час
        minutes: Минуты

    Returns:
        Объект времени.
    """
    return time(hour, minutes, 0, 0, get_tzinfo())
