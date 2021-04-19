"""Вспомогательные методы для работы с Google API."""
from os import path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

SCOPES = ('https://www.googleapis.com/auth/spreadsheets',)


def add_row_to_sheet(sheet_id: str, cells_range: str, table_name: str, row: list):
    """Добавление строки на лист.

    Parameters:
        sheet_id: Идентификатор таблицы
        cells_range: Рабочий диапазон ячеек
        table_name: Название листа таблицы
        row: Строка как массив ячеек
    """
    print(f'Attempt to write row {row} to sheet {table_name}')

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
    sheet_range = f'{table_name}!{cells_range}'
    request = sheet.values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={
            'values': [row],
        },
    )
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    print(response)
