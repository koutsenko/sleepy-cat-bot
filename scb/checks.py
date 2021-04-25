"""Матчинг сообщений."""
import itertools

from telegram import Message

from scb.tools_time import get_hour_msk, get_seconds_diff


def is_old_message(message: Message, last_event_time):
    """Проверка на старость сообщения (больше 5 минут с указанного момента).

    Parameters:
        message: Объект сообщения
        last_event_time: Момент, с которого отмерять время

    Returns:
        False если сообщение достаточно старое и можно реагировать
    """
    return (get_seconds_diff(last_event_time, message.date) / 60) > 5


def is_new_message(message: Message):
    """Проверка на свежесть сообщения (меньше минуты с текущего момента).

    Parameters:
        message: Объект сообщения

    Returns:
        False если сообщение слишком старое и не требует реакции

    """
    return get_seconds_diff(message.date) <= 60


def is_night_message(message: Message):
    """Обнаружение ночных (по Москве) сообщений.

    Parameters:
        message: Объект сообщения

    Returns:
        True если сообщение ночное

    """
    hour = get_hour_msk(message.date)
    night = itertools.chain(range(22, 24), range(0, 6))  # noqa: WPS432
    return hour in night
