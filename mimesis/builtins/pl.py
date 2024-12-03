"""Specific data provider for Poland (pl)."""
from mimesis.enums import Gender
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider, Datetime
from mimesis.types import DateTime, MissingSeed, Seed
__all__ = ['PolandSpecProvider']

class PolandSpecProvider(BaseDataProvider):
    """Class that provides special data for Poland (pl)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.PL, seed=seed)

    class Meta:
        name = 'poland_provider'
        datafile = None

    def nip(self) -> str:
        """Generate random valid 10-digit NIP.

        :return: Valid 10-digit NIP
        """
        weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
        nip = [self.random.randint(0, 9) for _ in range(9)]
        
        checksum = sum(w * d for w, d in zip(weights, nip)) % 11
        if checksum == 10:
            checksum = 0
        
        nip.append(checksum)
        return ''.join(map(str, nip))

    def pesel(self, birth_date: DateTime | None=None, gender: Gender | None=None) -> str:
        """Generate random 11-digit PESEL.

        :param birth_date: Initial birthdate (optional)
        :param gender: Gender of the person.
        :return: Valid 11-digit PESEL
        """
        if birth_date is None:
            birth_date = Datetime().datetime()
        
        if gender is None:
            gender = self.random.choice([Gender.MALE, Gender.FEMALE])
        
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        if 1800 <= year <= 1899:
            month += 80
        elif 2000 <= year <= 2099:
            month += 20
        elif 2100 <= year <= 2199:
            month += 40
        elif 2200 <= year <= 2299:
            month += 60
        
        pesel = f"{year % 100:02d}{month:02d}{day:02d}"
        pesel += f"{self.random.randint(0, 999):03d}"
        
        if gender == Gender.FEMALE:
            pesel += str(self.random.choice([0, 2, 4, 6, 8]))
        else:
            pesel += str(self.random.choice([1, 3, 5, 7, 9]))
        
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(p) * w for p, w in zip(pesel, weights))
        checksum = (10 - (checksum % 10)) % 10
        
        pesel += str(checksum)
        return pesel

    def regon(self) -> str:
        """Generate random valid 9-digit REGON.

        :return: Valid 9-digit REGON
        """
        weights = [8, 9, 2, 3, 4, 5, 6, 7]
        regon = [self.random.randint(0, 9) for _ in range(8)]
        
        checksum = sum(w * d for w, d in zip(weights, regon)) % 11
        if checksum == 10:
            checksum = 0
        
        regon.append(checksum)
        return ''.join(map(str, regon))
