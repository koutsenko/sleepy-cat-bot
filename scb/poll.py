"""Опрос о качестве сна."""
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import CallbackContext

from scb.google import add_row_to_sheet
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


def update_polls(polls, answer):
    """Обновление счетчика результатов в соответствии с ответом пользователя.

    Parameters:
        polls: Счетчик результатов
        answer: Ответ пользователя

    Returns:
        Новый массив с пересчитанными значениями счетчиков.
    """
    return [
        polls[0] + 1 if answer == '5' else polls[0],
        polls[1] + 1 if answer == '4' else polls[1],
        polls[2] + 1 if answer == '3' else polls[2],
        polls[3] + 1 if answer == '2' else polls[3],
    ]


def stop_poll(context: CallbackContext):
    """Остановка опроса - удаление кнопок и очистка контекста.

    Parameters:
        context: Контекст (память) бота

    """
    # TODO Проверка, что poll ранее состоялся
    context.bot.delete_message(
        chat_id=context.bot_data['poll_chat_id'],
        message_id=context.bot_data['poll_message_id'],
    )
    context.bot.send_message(
        chat_id=context.bot_data['poll_chat_id'],
        text=build_end_message(context.bot_data['poll_counters']),
    )
    context.bot_data.update({
        'poll_counters': None,
        'poll_chat_id': None,
        'poll_message_id': None,
        'poll_answered': None,
    })


def poll(context: CallbackContext):
    """Вывод опроса в чат.

    Parameters:
        context: Контекст (память) бота

    """
    channel_id = context.bot_data['config']['CHAT']
    polls = [0, 0, 0, 0]
    keyboard = build_keyboard(polls)
    question = 'Как спалось?'
    message: Message = context.bot.send_message(
        channel_id,
        text=question,
        reply_markup=keyboard,
    )
    context.bot_data.update({
        'poll_counters': polls,
        'poll_chat_id': message.chat_id,
        'poll_message_id': message.message_id,
    })


def write_poll(context: CallbackContext, user_id, user_name, answer):
    """Запись результата в гугл таблицу.

    Parameters:
        context: Контекст (память) бота
        user_id: ID пользователя
        user_name: Полное имя пользователя
        answer: Ответ пользователя

    """
    sheet_id = context.bot_data['config']['SHEET_ID']
    table_name = context.bot_data['config']['TABLE_NAME']
    cells_range = 'A2:E'
    row = [
        date.today().isoformat(),
        user_id,
        user_name,
        answer,
    ]
    add_row_to_sheet(sheet_id, cells_range, table_name, row)
