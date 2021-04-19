"""Обработка сообщений."""
import os
import signal
from datetime import datetime, timezone

from telegram import CallbackQuery, Update
from telegram.ext import CallbackContext

from scb.checks import is_new_message, is_night_message
from scb.google import add_row_to_sheet
from scb.poll import build_keyboard, poll, stop_poll, update_polls, write_poll
from scb.tools import pretty_print


def handle_message(update: Update, context: CallbackContext):
    """Обработка сообщений.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота

    """
    # Событие "Сообщение"
    if update.message:

        # Обработка только свежих
        if not is_new_message(update.message):
            return

        # Конфиг
        config = context.bot_data['config']

        # ID целевого канала и ID владельца
        channel_id = config['CHAT']
        owner_id = config['OWNER']

        # Обработка событий от себя
        if str(update.message.from_user.id) == owner_id:
            if update.message.text == 'sleepy cat quit':  # noqa: WPS223
                os.kill(os.getpid(), signal.SIGINT)
            elif update.message.text == 'ping':
                update.message.reply_text('pong')
            elif update.message.text == 'debug poll start':
                poll(context)
            elif update.message.text == 'debug poll stop':
                stop_poll(context)
            elif update.message.text == 'debug context':
                pretty_print(context.bot_data)
                pretty_print(context.user_data)
            elif update.message.text == 'check token':
                sheet_id = config['SHEET_ID']
                table_name = config['TABLE_TEST_NAME']
                cells_range = 'A1:A'
                row = ['проверочная строка']
                add_row_to_sheet(sheet_id, cells_range, table_name, row)

        # Обработка событий в целевом канале
        if str(update.message.chat.id) == channel_id:
            if is_night_message(update.message):
                handle_sleep_message(update, context)


def handle_poll_answer(update: Update, context: CallbackContext):
    """Обработка ответа на кнопки опроса.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота

    """
    query: CallbackQuery = update.callback_query
    query.answer()

    # Словарь признаков, что юзер user_id уже отвечал
    poll_answered = context.bot_data.get('poll_answered') or {}

    # Если уже отвечал, игнорируем
    if poll_answered.get(query.from_user.id):
        return

    # Обновление счетчиков
    polls = context.bot_data.get('poll_counters')
    polls_updated = update_polls(polls, query.data)

    # Вывод новых счетчиков в чат
    keyboard = build_keyboard(polls_updated)
    question = 'Как спалось?'
    query.edit_message_text(text=question, reply_markup=keyboard)

    # Обновляем контекст бота - счетчики и признаки
    context.bot_data.update({
        'poll_counters': polls_updated,
        'poll_answered': {
            **poll_answered,
            query.from_user.id: True,
        },
    })

    # Запись в гугл таблицы
    write_poll(
        context,
        query.from_user.id,
        query.from_user.full_name,
        query.data,
    )


def handle_sleep_message(update: Update, context: CallbackContext):
    """Обработка сообщений в полуночном чате.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота

    """
    # Время последнего напоминания от бота автору сообщения
    time = context.user_data.get('last_reminder_time')

    # Напоминание по условию
    if time is None or ((update.message.date - time).total_seconds() / 60) > 5:
        context.user_data['last_reminder_time'] = datetime.now(timezone.utc)
        update.message.reply_text('Пора спать!')
