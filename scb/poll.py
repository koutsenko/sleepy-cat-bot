"""Опрос о качестве сна."""
from datetime import date

from telegram import Message
from telegram.ext import CallbackContext

from scb.google import add_row_to_sheet
from scb.poll_helpers import build_end_message, build_keyboard


def check_poll_is_running(context: CallbackContext):
    """Проверка на уже запущенный опрос.

    Parameters:
        context: Контекст (память) бота

    Returns:
        True если опрос запущен.
    """
    return context.bot_data['poll_is_running'] is True


def start_poll(context: CallbackContext):
    """Вывод опроса в чат.

    Parameters:
        context: Контекст (память) бота

    """
    if check_poll_is_running(context):
        print('Ошибка запуска опроса - опрос уже был запущен')
        return

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
        'poll_is_running': True,
        'poll_counters': polls,
        'poll_chat_id': message.chat_id,
        'poll_message_id': message.message_id,
    })


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


def stop_poll(context: CallbackContext):
    """Остановка опроса - удаление кнопок и очистка контекста.

    Parameters:
        context: Контекст (память) бота

    """
    if not check_poll_is_running(context):
        print('Ошибка остановки опроса - не найден запущенный опрос')
        return

    chat_id = context.bot_data['poll_chat_id']
    message_id = context.bot_data['poll_message_id']
    text = build_end_message(context.bot_data['poll_counters'])

    context.bot.delete_message(chat_id, message_id)
    context.bot.send_message(chat_id, text)
    context.bot_data.update({
        'poll_is_running': None,
        'poll_counters': None,
        'poll_chat_id': None,
        'poll_message_id': None,
        'poll_answered': None,
    })
