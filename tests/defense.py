"""Тест модуля защиты."""
from scb.defense import build_engine, get_intent, get_response_by_intent


def test_defense():
    """Проверка базовой защиты."""
    engine = build_engine()

    # Проверка на призыв к убийству
    intent = get_intent(engine, 'Пристрелите кота')
    response = get_response_by_intent(engine, intent)
    assert response == ' '.join([
        'Нельзя стрелять в котиков!',
        'Как такая ужасная мысль пришла тебе в голову?',
        'Сон сделает тебя добрее, иди спать!',
    ])

    # Проверка на посыл в пешее далеко
    intent = get_intent(engine, 'Иди в жопу кот')
    response = get_response_by_intent(engine, intent)
    assert response == 'Ты такой злой, потому что плохо спишь. Иди спать!'

    # Проверка на обзывания
    intent = get_intent(engine, 'Тупой кот')
    response = get_response_by_intent(engine, intent)
    assert response == ' '.join([
        'Тупой будешь ты лет через 10,',
        'если не будешь соблюдать режим сна и бодрствования.',
        'Иди спать!',
    ])

    # Проверка на взбешенность
    intent = get_intent(engine, 'Меня достал кот')
    response = get_response_by_intent(engine, intent)
    assert response == 'Ты легко можешь решить эту проблему. Иди спать!'
