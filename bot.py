"""Ночной телеграм бот."""

import itertools
import json
import logging
import os
import signal
from datetime import datetime, timezone

import pytz
from dotenv import dotenv_values
from telegram import Bot, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater


def dump(source_obj):
    """Служебный метод для печати объекта в консоль.

    Parameters:
        source_obj: Объект на печать

    """
    print(json.dumps(source_obj, indent=4, sort_keys=True))


def is_new_message(message_utc_dt):
    """Проверка на свежесть сообщения.

    Parameters:
        message_utc_dt: DateTime время сообщения (UTC)

    Returns:
        False если сообщение слишком старое и не требует реакции

    """
    delta = datetime.now(timezone.utc) - message_utc_dt
    return delta.total_seconds() <= 60


def is_night_message(message_utc_dt):
    """Обнаружение ночных (по Москве) сообщений.

    Parameters:
        message_utc_dt: DateTime время сообщения (UTC)

    Returns:
        True если сообщение ночное

    """
    msk_dt = message_utc_dt.astimezone(tz=pytz.timezone('Europe/Moscow'))
    night = itertools.chain(range(22, 24), range(0, 6))  # noqa: WPS432
    return msk_dt.hour in night


def handle_message(update: Update, context: CallbackContext):
    """Обработка сообщений.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота

    """
    # Событие "Сообщение"
    if update.message:

        # Время и свежесть сообщения
        utc_dt = update.message.date
        fresh = is_new_message(utc_dt)

        # Обработка событий от себя
        if str(update.message.from_user.id) == config['OWNER']:
            if fresh and update.message.text == 'sleepy cat quit':
                os.kill(os.getpid(), signal.SIGINT)
            elif fresh and update.message.text == 'ping':
                update.message.reply_text('pong')

        # Обработка событий в целевом канале
        if str(update.message.chat.id) == config['CHAT']:
            if fresh and is_night_message(utc_dt):
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


# Настройка
config = dotenv_values('.env')
logging.basicConfig(level=logging.NOTSET)

# Инстанс бота и печать его основных свойств
bot = Bot(token=config['TOKEN'])
dump(bot.get_me().to_dict())

# Регистрация обработчика сообщений
updater = Updater(token=config['TOKEN'])
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
