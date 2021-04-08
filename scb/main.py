"""Ночной телеграм бот."""
import datetime
import logging

import pytz
from dotenv import dotenv_values
from telegram import Bot
from telegram.ext import Filters, MessageHandler, Updater

from scb.handlers import handle_message
from scb.pray import pray
from scb.tools import pretty_print


def main():
    """Точка входа."""
    # Настройка
    config = dotenv_values('.env')
    logging.basicConfig(level=logging.NOTSET)

    # Инстанс бота и печать его основных свойств
    bot = Bot(token=config['TOKEN'])
    pretty_print(bot.get_me().to_dict())

    # Регистрация обработчика сообщений
    updater = Updater(token=config['TOKEN'])
    updater.dispatcher.bot_data['config'] = config
    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))

    # Создание регулярных задач
    (ph, pm) = (22, 30)
    time = datetime.time(ph, pm, 0, 0, tzinfo=pytz.timezone('Europe/Moscow'))
    updater.job_queue.run_daily(pray, time)

    # Запуск
    updater.job_queue.start()
    updater.start_polling()
    updater.idle()
