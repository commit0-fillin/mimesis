"""Specific data provider for Ukraine (uk)."""
from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['UkraineSpecProvider']

class UkraineSpecProvider(BaseDataProvider):
    """Class that provides special data for Ukraine (uk)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.UK, seed=seed)

    class Meta:
        name = 'ukraine_provider'
        datafile = 'builtin.json'

    def patronymic(self, gender: Gender | None=None) -> str:
        """Generate random patronymic name.

        :param gender: Gender of person.
        :type gender: str or int
        :return: Patronymic name.
        """
        if gender is None:
            gender = self.random.choice([Gender.MALE, Gender.FEMALE])

        male_names = self.data['male_names']
        
        if gender == Gender.MALE:
            return self.random.choice(male_names)[:-1] + 'ович'
        elif gender == Gender.FEMALE:
            return self.random.choice(male_names)[:-1] + 'івна'
        else:
            raise ValueError("Invalid gender. Use Gender.MALE or Gender.FEMALE.")
