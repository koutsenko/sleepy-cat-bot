"""Вспомогательные функции для опроса о качестве сна."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from scb.today import build_today_message


def smile(polls, index):
    """Добавляет метку-смайлик к варианту опроса.

    Parameters:
        polls: Массив с результатами опроса
        index: Индекс варианта результата

    Returns:
        Значение счетчика с соответствующим смайликом.
    """
    return [
        f'😃 {polls[0]}',
        f'😏 {polls[1]}',
        f'😒 {polls[2]}',
        f'😡 {polls[3]}',
    ][index]


def build_keyboard(polls):
    """Сборка клавиатуры с текущими значениями счетчиков.

    Parameters:
        polls: Счетчик результатов

    Returns:
        Конфигурация пристегнутой к сообщению панели с кнопками.
    """
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text=smile(polls, 0), callback_data='5'),
        InlineKeyboardButton(text=smile(polls, 1), callback_data='4'),
        InlineKeyboardButton(text=smile(polls, 2), callback_data='3'),
        InlineKeyboardButton(text=smile(polls, 3), callback_data='2'),
    ]])


def build_end_message(polls):
    """Сборка текста сообщения при остановке опроса.

    Parameters:
        polls: Счетчик результатов

    Returns:
        Текст сообщения с текущими счетчиками и пожеланием хорошего дня.
    """
    today = f'\n\n{build_today_message()}.'
    wishes = '\nХорошего дня!'
    stats_indexes = list(range(4))
    stats_list = map(lambda index: smile(polls, index), stats_indexes)
    stats = ' '.join(stats_list)

    return f'Статистика сна:\n{stats}{today}{wishes}'
