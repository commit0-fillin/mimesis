"""Specific data provider for Russia (ru)."""
from datetime import datetime
from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['RussiaSpecProvider']

class RussiaSpecProvider(BaseDataProvider):
    """Class that provides special data for Russia (ru)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.RU, seed=seed)
        self._current_year = str(datetime.now().year)

    class Meta:
        """The name of the provider."""
        name = 'russia_provider'
        datafile = 'builtin.json'

    def generate_sentence(self) -> str:
        """Generate sentence from the parts.

        :return: Sentence.
        """
        subjects = ["Человек", "Кот", "Дом", "Город", "Ребенок"]
        verbs = ["видит", "любит", "строит", "изучает", "создает"]
        objects = ["мир", "будущее", "книгу", "картину", "технологию"]

        subject = self.random.choice(subjects)
        verb = self.random.choice(verbs)
        obj = self.random.choice(objects)

        return f"{subject} {verb} {obj}."

    def patronymic(self, gender: Gender | None=None) -> str:
        """Generate random patronymic name.

        :param gender: Gender of person.
        :return: Patronymic name.

        :Example:
            Алексеевна.
        """
        if gender is None:
            gender = self.random.choice([Gender.FEMALE, Gender.MALE])

        male_names = ["Александр", "Иван", "Петр", "Сергей", "Андрей"]
        female_endings = "овна евна ична"
        male_endings = "ович евич ич"

        base_name = self.random.choice(male_names)
        if gender == Gender.FEMALE:
            ending = self.random.choice(female_endings.split())
        else:
            ending = self.random.choice(male_endings.split())

        return f"{base_name}{ending}"

    def passport_series(self, year: int | None=None) -> str:
        """Generate random series of passport.

        :param year: Year of manufacture.
        :type year: int or None
        :return: Series.

        :Example:
            02 15.
        """
        if year is None:
            year = int(self._current_year[2:])
        else:
            year = year % 100

        region = self.random.randint(1, 99)
        return f"{region:02d} {year:02d}"

    def passport_number(self) -> int:
        """Generate random passport number.

        :return: Number.

        :Example:
            560430
        """
        return self.random.randint(100000, 999999)

    def series_and_number(self) -> str:
        """Generate a random passport number and series.

        :return: Series and number.

        :Example:
            57 16 805199.
        """
        series = self.passport_series()
        number = self.passport_number()
        return f"{series} {number}"

    def snils(self) -> str:
        """Generate snils with a special algorithm.

        :return: SNILS.

        :Example:
            41917492600.
        """
        def calculate_checksum(number):
            total = sum((9 - i) * int(digit) for i, digit in enumerate(number))
            if total < 100:
                return total
            elif total == 100 or total == 101:
                return 0
            else:
                return total % 101

        number = ''.join([str(self.random.randint(0, 9)) for _ in range(9)])
        checksum = calculate_checksum(number)
        return f"{number}{checksum:02d}"

    def inn(self) -> str:
        """Generate random, but valid ``INN``.

        :return: INN.
        """
        def calculate_checksum(number, coefficients):
            return str((sum(int(n) * c for n, c in zip(number, coefficients)) % 11) % 10)

        base = ''.join([str(self.random.randint(0, 9)) for _ in range(9)])
        n10 = calculate_checksum(base, (2, 4, 10, 3, 5, 9, 4, 6, 8))
        n11 = calculate_checksum(base + n10, (7, 2, 4, 10, 3, 5, 9, 4, 6, 8))
        return base + n10 + n11

    def ogrn(self) -> str:
        """Generate random valid ``OGRN``.

        :return: OGRN.

        :Example:
            4715113303725.
        """
        base = ''.join([str(self.random.randint(0, 9)) for _ in range(12)])
        check_digit = str((int(base) % 11) % 10)
        return base + check_digit

    def bic(self) -> str:
        """Generate random ``BIC`` (Bank ID Code).

        :return: BIC.

        :Example:
            044025575.
        """
        country_code = "04"  # Russia
        region_code = f"{self.random.randint(1, 99):02d}"
        bank_code = ''.join([str(self.random.randint(0, 9)) for _ in range(5)])
        return country_code + region_code + bank_code

    def kpp(self) -> str:
        """Generate random ``KPP``.

        :return: 'KPP'.

        :Example:
            560058652.
        """
        tax_authority = f"{self.random.randint(1, 9999):04d}"
        reason_code = f"{self.random.randint(1, 99):02d}"
        registration_number = f"{self.random.randint(1, 999):03d}"
        return tax_authority + reason_code + registration_number
