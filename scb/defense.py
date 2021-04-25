"""Защита, если на котобота матерятся."""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def build_engine():
    """Создание движка с поддержкой ответов на разные виды наездов и ругательств.

    Returns:
        Обученная модель
    """
    engine = {
        'classifier_treshold': 0.4,
        'classifier': LogisticRegression(),
        'offence_intents': {
            'shoot': ['Пристрелите кота'],
            'send': ['Иди в жопу кот', 'Пошел нахуй'],
            'dumb': ['Тупой кот'],
            'pissed': ['Меня достал кот'],
        },
        'offence_responses': {
            'shoot': ' '.join([
                'Нельзя стрелять в котиков!',
                'Как такая ужасная мысль пришла тебе в голову?',
                'Сон сделает тебя добрее, иди спать!',
            ]),
            'send': 'Ты такой злой, потому что плохо спишь. Иди спать!',
            'dumb': ' '.join([
                'Тупой будешь ты лет через 10,',
                'если не будешь соблюдать режим сна и бодрствования.',
                'Иди спать!',
            ]),
            'pissed': 'Ты легко можешь решить эту проблему. Иди спать!',
        },
        'vectorizer': CountVectorizer(),
    }
    study(engine)
    return engine


def study(engine):
    """Обучение классификатора сообщений.

    Parameters:
        engine: Движок

    """
    classes = []
    phrases = []

    for intent, phrase_list in engine['offence_intents'].items():
        for phrase in phrase_list:
            phrases.append(phrase)
            classes.append(intent)

    engine['classifier'].fit(
        engine['vectorizer'].fit_transform(phrases),
        classes,
    )


def get_intent(engine, text):
    """Распознавание вида сообщения.

    Parameters:
        engine: Движок
        text: Сообщение

    Returns:
        Вид сообщения или None, если не удалось распознать
    """
    classifier = engine['classifier']
    vector = engine['vectorizer'].transform([text])
    probas = classifier.predict_proba(vector)
    max_proba = max(probas[0])
    if max_proba >= engine['classifier_treshold']:
        index = list(probas[0]).index(max_proba)
        return classifier.classes_[index]


def get_response_by_intent(engine, intent):
    """Поиск ответа.

    Parameters:
        engine: Движок
        intent: Вид сообщения

    Returns:
        Текст ответа
    """
    return engine['offence_responses'][intent]


def handle_offensive_message(engine, message: str):
    """Обработка сообщения.

    Parameters:
        engine: Движок
        message: Сообщение

    Returns:
        Текст ответа
    """
    intent = get_intent(engine, message)
    if intent:
        return get_response_by_intent(engine, intent)
