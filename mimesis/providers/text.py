"""Provides data related to text."""
import typing as t
from mimesis.datasets import SAFE_COLORS
from mimesis.enums import EmojyCategory
from mimesis.providers.base import BaseDataProvider
__all__ = ['Text']

class Text(BaseDataProvider):
    """Class for generating text data."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize attributes."""
        super().__init__(*args, **kwargs)
        self._emojis = self._read_global_file('emojis.json')

    class Meta:
        name = 'text'
        datafile = f'{name}.json'

    def alphabet(self, lower_case: bool=False) -> list[str]:
        """Returns an alphabet for current locale.

        :param lower_case: Return alphabet in lower case.
        :return: Alphabet.
        """
        alphabet = self._dataset['alphabet']
        if lower_case:
            return [letter.lower() for letter in alphabet]
        return alphabet

    def level(self) -> str:
        """Generates a word that indicates a level of something.

        :return: Level.

        :Example:
            critical.
        """
        return self.random.choice(self._dataset['level'])

    def text(self, quantity: int=5) -> str:
        """Generates the text.

        :param quantity: Quantity of sentences.
        :return: Text.
        """
        return ' '.join(self.sentence() for _ in range(quantity))

    def sentence(self) -> str:
        """Generates a random sentence from the text.

        :return: Sentence.
        """
        words = self.words(quantity=self.random.randint(5, 10))
        sentence = ' '.join(words).capitalize() + '.'
        return sentence

    def title(self) -> str:
        """Generates a random title.

        :return: The title.
        """
        words = self.words(quantity=self.random.randint(2, 5))
        return ' '.join(word.capitalize() for word in words)

    def words(self, quantity: int=5) -> list[str]:
        """Generates a list of random words.

        :param quantity: Quantity of words. Default is 5.
        :return: Word list.

        :Example:
            [science, network, god, octopus, love]
        """
        words = self._dataset['words']
        return self.random.choices(words, k=quantity)

    def word(self) -> str:
        """Generates a random word.

        :return: Single word.

        :Example:
            Science.
        """
        return self.random.choice(self._dataset['words'])

    def quote(self) -> str:
        """Generates a random quote.

        :return: Random quote.

        :Example:
            "Bond... James Bond."
        """
        return self.random.choice(self._dataset['quotes'])

    def color(self) -> str:
        """Generates a random color name.

        :return: Color name.

        :Example:
            Red.
        """
        return self.random.choice(self._dataset['color'])

    @staticmethod
    def _hex_to_rgb(color: str) -> tuple[int, ...]:
        """Converts hex color to RGB format.

        :param color: Hex color.
        :return: RGB tuple.
        """
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    def hex_color(self, safe: bool=False) -> str:
        """Generates a random HEX color.

        :param safe: Get safe Flat UI hex color.
        :return: Hex color code.

        :Example:
            #d8346b
        """
        if safe:
            return self.random.choice(SAFE_COLORS)
        return '#{:06x}'.format(self.random.randint(0, 0xFFFFFF))

    def rgb_color(self, safe: bool=False) -> tuple[int, ...]:
        """Generates a random RGB color tuple.

        :param safe: Get safe RGB tuple.
        :return: RGB tuple.

        :Example:
            (252, 85, 32)
        """
        hex_color = self.hex_color(safe)
        return self._hex_to_rgb(hex_color)

    def answer(self) -> str:
        """Generates a random answer in the current language.

        :return: An answer.

        :Example:
            No
        """
        return self.random.choice(self._dataset['answers'])

    def emoji(self, category: EmojyCategory | None=EmojyCategory.DEFAULT) -> str:
        """Generates a random emoji from the specified category.

        Generates a random emoji from the specified category.
        If the category is not specified, a random emoji
        from any category will be returned.

        :param category: :class:`~mimesis.enums.EmojyCategory`.
        :raises NonEnumerableError: When category is not supported.
        :return: Emoji code.
        :example:
            😟
        """
        category = self.validate_enum(category, EmojyCategory)
        if category == EmojyCategory.DEFAULT:
            return self.random.choice([emoji for emojis in self._emojis.values() for emoji in emojis])
        return self.random.choice(self._emojis[category.value])
