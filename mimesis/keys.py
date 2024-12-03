"""The module **mimesis.keys** provides a set of key functions.

Key functions can be applied to fields and fieldsets using the **key** argument.
These functions are applied after the field's value is generated and before the
field is returned to the caller.
"""
from typing import Any, Callable
from mimesis.datasets import COMMON_LETTERS, ROMANIZATION_DICT
from mimesis.locales import Locale, validate_locale
from mimesis.random import Random
__all__ = ['maybe', 'romanize']

def romanize(locale: Locale) -> Callable[[str], str]:
    """Create a closure function to romanize a given string in the specified locale.

    Supported locales are:

    - Locale.RU (Russian)
    - Locale.UK (Ukrainian)
    - Locale.KK (Kazakh)

    :param locale: Locale.
    :return: A closure that takes a string and returns a romanized string.
    """
    validate_locale(locale)
    
    def _romanize(text: str) -> str:
        romanization_map = ROMANIZATION_DICT.get(locale, {})
        return ''.join(romanization_map.get(char, char) for char in text)
    
    return _romanize

def maybe(value: Any, probability: float=0.5) -> Callable[[Any, Random], Any]:
    """Return a closure (a key function).

    The returned closure itself returns either **value** or
    the first argument passed to closure with a certain probability (0.5 by default).

    :param value: The value that may be returned.
    :param probability: The probability of returning **value**.
    :return: A closure that takes two arguments.
    """
    def _maybe(arg: Any, random: Random) -> Any:
        return value if random.random() < probability else arg
    
    return _maybe
