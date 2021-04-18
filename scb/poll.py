"""Опрос о качестве сна."""
from datetime import date
from os import path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import CallbackContext

SCOPES = ('https://www.googleapis.com/auth/spreadsheets',)


def build_keyboard(polls):
    """Сборка клавиатуры с текущими значениями счетчиков.

    Parameters:
        polls: Счетчик результатов

    Returns:
        Конфигурация пристегнутой к сообщению панели с кнопками.
    """
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text=f'😃 {polls[0]}', callback_data='5'),
        InlineKeyboardButton(text=f'😏 {polls[1]}', callback_data='4'),
        InlineKeyboardButton(text=f'😒 {polls[2]}', callback_data='3'),
        InlineKeyboardButton(text=f'😡 {polls[3]}', callback_data='2'),
    ]])


def build_end_message(polls):
    """Сборка текста сообщения при остановке опроса.

    Parameters:
        polls: Счетчик результатов

    Returns:
        Текст сообщения с текущими счетчиками и пожеланием хорошего дня.
    """
    st = 'Статистика сна:\n'
    sp = '   '
    r5 = f'😃 {polls[0]}'
    r4 = f'😏 {polls[1]}'
    r3 = f'😒 {polls[2]}'
    r2 = f'😡 {polls[3]}'
    end = '\n\nХорошего дня!'

    return f'{st}{r5}{sp}{r4}{sp}{r3}{sp}{r2}{end}'


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


def stop_poll(context: CallbackContext):
    """Остановка опроса - удаление кнопок и очистка контекста.

    Parameters:
        context: Контекст (память) бота

    """
    # TODO Проверка, что poll ранее состоялся
    context.bot.edit_message_text(
        chat_id=context.bot_data['poll_chat_id'],
        message_id=context.bot_data['poll_message_id'],
        text=build_end_message(context.bot_data['poll_counters']),
    )
    context.bot_data.update({
        'poll_counters': None,
        'poll_chat_id': None,
        'poll_message_id': None,
        'poll_answered': None,
    })


def poll(context: CallbackContext):
    """Вывод опроса в чат.

    Parameters:
        context: Контекст (память) бота

    """
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
        'poll_counters': polls,
        'poll_chat_id': message.chat_id,
        'poll_message_id': message.message_id,
    })


def write_poll(context: CallbackContext, user_id, user_name, answer):
    """Запись результата в гугл таблицу.

    Parameters:
        context: Контекст (память) бота
        user_id: ID пользователя
        user_name: Полное имя пользователя
        answer: Ответ пользователя

    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service: Resource = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Append rows
    sheet_id = context.bot_data['config']['SHEET_ID']
    table_name = context.bot_data['config']['TABLE_NAME']
    sheet_range = f'{table_name}!A2:E'
    request = sheet.values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={
            'values': [[
                date.today().isoformat(),
                user_id,
                user_name,
                answer,
            ]],
        },
    )
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    print(response)