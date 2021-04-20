"""Обработка сообщений от владельца бота."""
import os
import signal

from telegram import Update
from telegram.ext import CallbackContext

from scb.google import add_row_to_sheet
from scb.poll import build_end_message, poll, stop_poll
from scb.tools import pretty_print


def handle_owner_message(update: Update, context: CallbackContext):
    """Обработка сообщений от владельца бота.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота
    """
    text = update.message.text

    if not text:
        return

    if text == 'sleepy cat quit':
        os.kill(os.getpid(), signal.SIGINT)
    elif text == 'ping':
        update.message.reply_text('pong')
    elif text.startswith('debug '):
        handle_owner_debug_message(update, context)


def handle_owner_debug_message(update: Update, context: CallbackContext):
    """Обработка отладочных сообщений от владельца бота.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота
    """
    sheet_id = context.bot_data['config']['SHEET_ID']
    table_name = context.bot_data['config']['TABLE_TEST_NAME']
    text = update.message.text

    if text.startswith('debug poll '):
        handle_owner_debug_poll_message(update, context)
    elif text == 'debug context':
        pretty_print(context.bot_data)
        pretty_print(context.user_data)
    elif text == 'debug google sheets write':
        cells_range = 'A1:A'
        row = ['проверочная строка']
        add_row_to_sheet(sheet_id, cells_range, table_name, row)


def handle_owner_debug_poll_message(update: Update, context: CallbackContext):
    """Обработка отладочных сообщений опроса от владельца бота.

    Parameters:
        update: Событие сообщения
        context: Контекст (память) бота
    """
    text = update.message.text

    if text == 'debug poll start':
        poll(context)
    elif text == 'debug poll stop':
        stop_poll(context)
    elif text == 'debug poll stats print':
        update.message.reply_text(build_end_message([2, 5, 1, 0]))
