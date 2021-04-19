"""Ночной телеграм бот."""
import datetime
import logging

import pytz
from dotenv import dotenv_values
from telegram import Bot
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater

from scb.handlers import handle_message, handle_poll_answer
from scb.poll import poll, stop_poll
from scb.pray import pray
from scb.tools import pretty_print


def main():
    """Точка входа."""
    # Настройка
    config = dotenv_values('.env')
    logging.basicConfig(filename='bot.log', level=logging.NOTSET)

    # Инстанс бота и печать его основных свойств
    bot = Bot(token=config['TOKEN'])
    pretty_print(bot.get_me().to_dict())

    # Регистрация обработчика сообщений
    updater = Updater(token=config['TOKEN'])
    updater.dispatcher.bot_data['config'] = config
    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_poll_answer))

    # Создание регулярных задач
    tzinfo = pytz.timezone('Europe/Moscow')
    jobs = [
        [22, 30, pray],
        [8, 30, poll],
        [12, 00, stop_poll],
    ]
    for job in jobs:
        time = datetime.time(job[0], job[1], 0, 0, tzinfo)
        updater.job_queue.run_daily(job[2], time)

    # Запуск
    updater.job_queue.start()
    updater.start_polling()
    updater.idle()
