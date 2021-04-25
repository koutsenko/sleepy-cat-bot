"""Функции для работы с датой и временем."""
from datetime import datetime, time, timezone

import pytz


def get_timezone():
    """Таймзона бота.

    Returns:
        Таймзона.
    """
    return pytz.timezone('Europe/Moscow')


def get_time(hour: int, minutes: int):
    """Сбор объекта времени.

    Parameters:
        hour: Час
        minutes: Минуты

    Returns:
        Объект времени.
    """
    return time(hour, minutes, 0, 0, get_timezone())


def get_week_day():
    """Текущий день недели.

    Returns:
        Число дня недели, начиная с 0.
    """
    day_local = datetime.utcnow().astimezone(get_timezone())
    today = day_local.today()

    return today.weekday()


def get_seconds_diff(dt_from: datetime, dt_to: datetime = None):
    """Разница в секундах между штампами времени.

    Parameters:
        dt_from: Время начала
        dt_to: Время конца, если не указан, используется текущее время

    Returns:
        Кол-во секунд.
    """
    delta = None
    if dt_to is None:
        delta = datetime.now(timezone.utc) - dt_from
    else:
        delta = dt_to - dt_from

    return delta.total_seconds()


def get_hour_msk(dt: datetime):
    """Текущий час по Москве.

    Parameters:
        dt: Время

    Returns:
        Час.
    """
    return dt.astimezone(get_timezone()).hour


def get_now_utc():
    """Текущее время UTC.

    Returns:
        Штмп времени.
    """
    return datetime.now(timezone.utc)
