"""Молитва."""
from os import getcwd, path

from telegram.ext import CallbackContext


def pray(context: CallbackContext):
    """Молитва в целевой чат.

    Parameters:
        context: Контекст (память) бота

    """
    # Пути к скрипту и файлу с молитвой
    script_path = path.realpath(path.join(getcwd(), path.dirname(__file__)))
    pray_path = path.join(script_path, 'pray.txt')

    # Чтение из файла (будет закрыт автоматически) и вывод в чат
    with open(pray_path, 'r', encoding='utf-8') as pray_file:
        pray_text = pray_file.read()
        channel_id = context.bot_data['config']['CHAT']
        context.bot.send_message(chat_id=channel_id, text=pray_text)
