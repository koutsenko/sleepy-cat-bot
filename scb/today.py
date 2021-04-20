"""Утренняя инфа про сегодняшний день."""
from datetime import datetime

import pytz

days = [
    'понедельник, день прокрастинации',
    'вторник, день докапывания',
    'среда, день занудства',
    'четверг, день смерти',
    'пятница, обычный день',
    'суббота, день нытья',
    'воскресенье, обычный день',
]


def build_today_message():
    """Напоминание о том какой сегодня день.

    Returns:
        Текст информации о сегодняшнем дне.
    """
    day_local = datetime.utcnow().astimezone(tz=pytz.timezone('Europe/Moscow'))
    weekday = day_local.today().weekday()

    return f'Сегодня {days[weekday]}'


if __name__ == '__main__':
    print(build_today_message())
