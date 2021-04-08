"""Ночной телеграм бот."""
import logging

from dotenv import dotenv_values
from telegram import Bot
from telegram.ext import Filters, MessageHandler, Updater

from scb.handlers import handle_message
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
    updater.start_polling()
    updater.idle()
