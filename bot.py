"""Ночной телеграм бот."""

import json

import telegram
from dotenv import dotenv_values

config = dotenv_values('.env')

bot = telegram.Bot(token=config['TOKEN'])

about = bot.get_me().to_dict()
print(json.dumps(about, indent=4, sort_keys=True))
