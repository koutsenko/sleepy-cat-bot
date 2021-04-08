"""Утилиты."""

import json


def pretty_print(source_obj):
    """Служебный метод для печати объекта в консоль.

    Parameters:
        source_obj: Объект на печать

    """
    print(json.dumps(source_obj, indent=4, sort_keys=True))
