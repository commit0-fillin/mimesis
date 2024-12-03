"""Implements various helpers which are used in the various data providers.

This module contains custom ``Random()`` class where implemented a lot of
methods which are not included in standard :py:class:`random.Random`,
but frequently used in this project.
"""
import random as random_module
import typing as t
from mimesis.types import MissingSeed, Seed
__all__ = ['Random', 'random']
global_seed: Seed = MissingSeed

class Random(random_module.Random):
    """A custom random class.

    It is a subclass of the :py:class:`random.Random` class from the standard
    library's random module. The class incorporates additional custom methods.

    This class can be extended according to specific requirements.
    """

    def randints(self, n: int=3, a: int=1, b: int=100) -> list[int]:
        """Generate a list of random integers.

        :param n: Number of elements.
        :param a: Minimum value of range.
        :param b: Maximum value of range.
        :return: List of random integers.
        :raises ValueError: if the number is less or equal to zero.
        """
        if n <= 0:
            raise ValueError("Number of elements must be greater than zero.")
        return [self.randint(a, b) for _ in range(n)]

    def _generate_string(self, str_seq: str, length: int=10) -> str:
        """Generate random string created from a string sequence.

        :param str_seq: String sequence of letters or digits.
        :param length: Max value.
        :return: Single string.
        """
        return ''.join(self.choice(str_seq) for _ in range(length))

    def generate_string_by_mask(self, mask: str='@###', char: str='@', digit: str='#') -> str:
        """Generate custom code using ascii uppercase and random integers.

        :param mask: Mask of code.
        :param char: Placeholder for characters.
        :param digit: Placeholder for digits.
        :return: Custom code.
        """
        char_sequence = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digit_sequence = '0123456789'
        return ''.join(self.choice(char_sequence) if c == char else
                       self.choice(digit_sequence) if c == digit else c
                       for c in mask)

    def uniform(self, a: float, b: float, precision: int=15) -> float:
        """Get a random number in the range [a, b) or [a, b] depending on rounding.

        :param a: Minimum value.
        :param b: Maximum value.
        :param precision: Round a number to a given
            precision in decimal digits, default is 15.
        """
        return round(super().uniform(a, b), precision)

    def randbytes(self, n: int=16) -> bytes:
        """Generate n random bytes."""
        return bytes(self.randint(0, 255) for _ in range(n))

    def weighted_choice(self, choices: dict[t.Any, float]) -> t.Any:
        """Returns a random element according to the specified weights.

        :param choices: A dictionary where keys are choices and values are weights.
        :raises ValueError: If choices are empty.
        :return: Random key from dictionary.
        """
        if not choices:
            raise ValueError("Choices dictionary cannot be empty.")
        total = sum(choices.values())
        r = self.uniform(0, total)
        for choice, weight in choices.items():
            r -= weight
            if r <= 0:
                return choice

    def choice_enum_item(self, enum: t.Any) -> t.Any:
        """Get random value of enum object.

        :param enum: Enum object.
        :return: Random value of enum.
        """
        return self.choice(list(enum))
random = Random()
