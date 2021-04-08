"""Обработка сообщений."""
import os
import signal
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import CallbackContext

from scb.checks import is_new_message, is_night_message


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

        # ID целевого канала и ID владельца
        channel_id = context.bot_data['config']['CHAT']
        owner_id = context.bot_data['config']['OWNER']

        # Обработка событий от себя
        if str(update.message.from_user.id) == owner_id:
            if update.message.text == 'sleepy cat quit':
                os.kill(os.getpid(), signal.SIGINT)
            elif update.message.text == 'ping':
                update.message.reply_text('pong')

        # Обработка событий в целевом канале
        if str(update.message.chat.id) == channel_id:
            if is_night_message(update.message):
                handle_sleep_message(update, context)


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
