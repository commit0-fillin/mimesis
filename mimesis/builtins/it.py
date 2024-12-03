"""Specific data provider for Italy (it)."""
import string
from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['ItalySpecProvider']

class ItalySpecProvider(BaseDataProvider):
    """Specific-provider of misc data for Italy."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.IT, seed=seed)

    class Meta:
        name = 'italy_provider'
        datafile = 'builtin.json'

    def fiscal_code(self, gender: Gender | None=None) -> str:
        """Return a random fiscal code.

        :param gender: Gender's enum object.
        :return: Fiscal code.

        Example:
            RSSMRA66R05D612U
        """
        # Generate surname (3 letters)
        surname = ''.join(self.random.choices(string.ascii_uppercase, k=3))

        # Generate name (3 letters)
        name = ''.join(self.random.choices(string.ascii_uppercase, k=3))

        # Generate birth year (2 digits)
        year = self.random.randint(0, 99)

        # Generate birth month (1 letter)
        month = self.random.choice('ABCDEHLMPRST')

        # Generate birth day (2 digits)
        day = self.random.randint(1, 31)
        if gender == Gender.FEMALE:
            day += 40

        # Generate place code (4 alphanumeric characters)
        place = ''.join(self.random.choices(string.ascii_uppercase + string.digits, k=4))

        # Generate check character
        code = f"{surname}{name}{year:02d}{month}{day:02d}{place}"
        even_sum = sum(int(c) if c.isdigit() else ord(c) - 55 for c in code[1::2])
        odd_sum = sum([1, 0, 5, 7, 9, 13, 15, 17, 19, 21][int(c)] if c.isdigit() else [1, 0, 5, 7, 9, 13, 15, 17, 19, 21][ord(c) - 65] for c in code[::2])
        check = chr((even_sum + odd_sum) % 26 + 65)

        return f"{code}{check}"
