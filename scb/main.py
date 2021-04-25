"""Ночной телеграм бот."""
import logging

from dotenv import dotenv_values
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater

from scb.handlers import handle_message, handle_poll_answer
from scb.poll import start_poll, stop_poll
from scb.pray import pray
from scb.tools import pretty_print
from scb.tools_time import get_time


def main():
    """Точка входа."""
    # Настройка
    config = dotenv_values('.env')
    logging.basicConfig(filename='bot.log', level=logging.NOTSET)

    # Фронтенд для telegram.Bot
    updater = Updater(token=config['TOKEN'])

    # Инициализация контекста
    updater.dispatcher.bot_data['config'] = config

    # Регистрация обработчика сообщений
    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_poll_answer))

    # Создание регулярных задач
    jobs = [
        [22, 30, pray],
        [8, 30, start_poll],
        [10, 00, stop_poll],
    ]
    for job in jobs:
        job_time = get_time(job[0], job[1])
        updater.job_queue.run_daily(job[2], job_time)

    # Печать основных свойств бота
    pretty_print(updater.bot.get_me().to_dict())

    # Запуск
    updater.job_queue.start()
    updater.start_polling()
    updater.idle()
