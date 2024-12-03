"""Specific data provider for Denmark (da)."""
import operator
from mimesis import Datetime
from mimesis.locales import Locale
from mimesis.providers import BaseDataProvider
from mimesis.types import MissingSeed, Seed
__all__ = ['DenmarkSpecProvider']

class DenmarkSpecProvider(BaseDataProvider):
    """Class that provides special data for Denmark (da)."""

    def __init__(self, seed: Seed=MissingSeed) -> None:
        """Initialize attributes."""
        super().__init__(locale=Locale.DA, seed=seed)
        self._datetime = Datetime(locale=Locale.DA, seed=seed, random=self.random)
        self._checksum_factors = (4, 3, 2, 7, 6, 5, 4, 3, 2)

    class Meta:
        name = 'denmark_provider'
        datafile = None

    def _calculate_checksum(self, cpr_nr_no_checksum: str) -> int:
        """Calculate the CPR number checksum.

        The CPR checksum can be checked by:
        1. Multiplying each digit in the CPR number with a corresponding fixed
           factor (self._checksum_factors) to produce a list of products.
        2. Summing up all the products, including the checksum, and checking
           that the resulting sum modulo 11 is 0.

        As such the checksum can be determined by reordering the formula, as:
        * 11 - (sum_without_checksum % 11)

        If the sum_without_checksum is 0, the resulting checksum is 11, but
        returned as 0 according to the official rules.

        If the sum_without_checksum is 1, the resulting checksum is 10, and
        thus invalid as the checksum is only 1 digit, hence this implies that
        the generated serial_number is invalid.

        Note: This method does not handle checksum == 10 case.
              It is handled by recursion in _generate_serial_checksum.
        """
        sum_without_checksum = sum(int(digit) * factor for digit, factor in zip(cpr_nr_no_checksum, self._checksum_factors))
        checksum = 11 - (sum_without_checksum % 11)
        
        if checksum == 11:
            return 0
        return checksum

    def _generate_serial_checksum(self, cpr_century: str) -> tuple[str, int]:
        """Generate a serial number and checksum from cpr_century."""
        while True:
            serial_number = ''.join(str(self.random.randint(0, 9)) for _ in range(3))
            cpr_nr_no_checksum = cpr_century + serial_number
            checksum = self._calculate_checksum(cpr_nr_no_checksum)
            
            if checksum != 10:
                return serial_number, checksum

    def cpr(self) -> str:
        """Generate a random CPR number (Central Person Registry).

        :return: CPR number.

        :Example:
            0405420694
        """
        birth_date = self._datetime.date(start=1900, end=2099)
        day = f"{birth_date.day:02d}"
        month = f"{birth_date.month:02d}"
        year = str(birth_date.year)[-2:]
        
        cpr_century = day + month + year
        
        if birth_date.year >= 2000:
            cpr_century = day + month + year
        
        serial_number, checksum = self._generate_serial_checksum(cpr_century)
        
        return f"{cpr_century}{serial_number}{checksum}"
