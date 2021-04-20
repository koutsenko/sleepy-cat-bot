"""Матчинг сообщений."""
import itertools
from datetime import datetime, timezone

import pytz
from telegram import Message


def is_old_message(message: Message, last_event_time):
    """Проверка на старость сообщения (больше 5 минут с указанного момента).

    Parameters:
        message: Объект сообщения
        last_event_time: Момент, с которого отмерять время

    Returns:
        False если сообщение достаточно старое и можно реагировать
    """
    delta = message.date - last_event_time
    return (delta.total_seconds() / 60) > 5


def is_new_message(message: Message):
    """Проверка на свежесть сообщения (меньше минуты с текущего момента).

    Parameters:
        message: Объект сообщения

    Returns:
        False если сообщение слишком старое и не требует реакции

    """
    delta = datetime.now(timezone.utc) - message.date
    return delta.total_seconds() <= 60


def is_night_message(message: Message):
    """Обнаружение ночных (по Москве) сообщений.

    Parameters:
        message: Объект сообщения

    Returns:
        True если сообщение ночное

    """
    msk_dt = message.date.astimezone(tz=pytz.timezone('Europe/Moscow'))
    night = itertools.chain(range(22, 24), range(0, 6))  # noqa: WPS432
    return msk_dt.hour in night
